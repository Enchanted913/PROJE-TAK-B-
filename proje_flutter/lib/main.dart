import 'package:flutter/material.dart';
import 'config.dart';
import 'screens/home_screen.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/students_list_screen.dart';
import 'screens/projects_list_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final auth = AuthProvider();
  await auth.loadFromStorage();
  runApp(MyApp(auth: auth));
}

class MyApp extends StatelessWidget {
  final AuthProvider auth;
  const MyApp({super.key, required this.auth});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: auth,
      child: MaterialApp(
        title: 'TurkTicaret App',
        theme: appTheme,
        home: Consumer<AuthProvider>(builder: (context, auth, _) {
          if (auth.token != null) return const ProjectsListScreen();
          return const LoginScreen();
        }),
        routes: {
          '/login': (_) => const LoginScreen(),
          '/register': (_) => const RegisterScreen(),
          '/students': (_) => const StudentsListScreen(),
          '/projects': (_) => const ProjectsListScreen(),
          '/home': (_) => const HomeScreen(),
        },
      ),
    );
  }
}
