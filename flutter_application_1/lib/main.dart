import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'segunda_tela.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meu Primeiro App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const TelaDeRegistro(),
    );
  }
}

class TelaDeRegistro extends StatefulWidget {
  const TelaDeRegistro({super.key});

  @override
  State<TelaDeRegistro> createState() => _TelaDeRegistroState();
}

class _TelaDeRegistroState extends State<TelaDeRegistro> {
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  String _statusMessage = '';

  Future _registrar() async {
    final response = await http.post(
      Uri.parse('http://localhost:5000/register'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'name': usernameController.text,
        'email': emailController.text,
        'password': passwordController.text,
      }),
    );

    if (response.statusCode == 201) { // 201 para created
      setState(() {
        _statusMessage = 'Usuário registrado: ${usernameController.text}';
      });
      print("Usuário registrado");
    } else {
      setState(() {
        _statusMessage = 'Erro ao registrar usuário';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tela de Registro'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              controller: usernameController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Nome de usuário',
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Email',
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Senha',
              ),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _registrar,
              child: const Text('Registrar'),
            ),
            const SizedBox(height: 20),
            Text(
              _statusMessage,
              style: const TextStyle(fontSize: 18, color: Colors.green),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const TelaDeLogin()),
                );
              },
              child: const Text("Ir para Login"),
            ),
          ],
        ),
      ),
    );
  }
}
