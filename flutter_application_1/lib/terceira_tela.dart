import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:convert';

class TelaDeConteudo extends StatefulWidget {
  const TelaDeConteudo({super.key});

  @override
  _TelaDeConteudoState createState() => _TelaDeConteudoState();
}

class _TelaDeConteudoState extends State<TelaDeConteudo> {
  File? _image;
  String? _webImage;
  XFile? _webXFile;
  String? _processedImageUrl;

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        if (kIsWeb) {
          _webImage = pickedFile.path;
          _webXFile = pickedFile;
        } else {
          _image = File(pickedFile.path);
        }
      });
    }
  }

  Future<void> _uploadImage() async {
    if (_image == null && _webXFile == null) return;

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://localhost:5002/upload'),
    );

    if (kIsWeb) {
      final bytes = await _webXFile!.readAsBytes();
      final stream = http.ByteStream.fromBytes(bytes);
      final length = bytes.length;
      final multipartFile = http.MultipartFile(
        'file',
        stream,
        length,
        filename: _webXFile!.name,
        contentType: MediaType('application', 'octet-stream'),
      );
      request.files.add(multipartFile);
    } else {
      request.files.add(await http.MultipartFile.fromPath('file', _image!.path));
    }

    final response = await request.send();

    if (response.statusCode == 200) {
      final responseData = await http.Response.fromStream(response);
      final data = jsonDecode(responseData.body);
      setState(() {
        _processedImageUrl = 'http://localhost:5002/uploads/' + data['processed_image'];
      });
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ProcessedImageScreen(imageUrl: _processedImageUrl!),
        ),
      );
    } else {
      print('Image upload failed');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ACESSADO! BEM-VINDO'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'BEM-VINDO À APLICAÇÃO',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 20),
            kIsWeb
                ? _webImage == null
                    ? const Text('Nenhuma imagem selecionada.')
                    : Image.network(_webImage!)
                : _image == null
                    ? const Text('Nenhuma imagem selecionada.')
                    : Image.file(_image!),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('Selecionar Imagem'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _uploadImage,
              child: const Text('Upload Imagem'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  PageRouteBuilder(
                    pageBuilder: (context, animation1, animation2) => const TelaDeConteudo(),
                    transitionDuration: Duration.zero,
                    reverseTransitionDuration: Duration.zero,
                  ),
                );
              },
              child: const Text("Atualizar Página"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text("Voltar"),
            ),
          ],
        ),
      ),
    );
  }
}

class ProcessedImageScreen extends StatelessWidget {
  final String imageUrl;

  const ProcessedImageScreen({super.key, required this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Imagem Processada'),
      ),
      body: Center(
        child: Image.network(imageUrl),
      ),
    );
  }
}
