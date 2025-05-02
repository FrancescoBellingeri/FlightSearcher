import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000'; // Modifica con il tuo URL

  Future<dynamic> searchFlights(Map<String, dynamic> searchParams) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/search'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(searchParams),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to search flights');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}