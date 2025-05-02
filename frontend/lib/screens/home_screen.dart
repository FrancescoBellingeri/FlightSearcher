import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import 'package:month_picker_dialog/month_picker_dialog.dart';
import '../models/flight_result.dart';
import 'results_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // Sposta queste variabili qui
  final ApiService _apiService = ApiService();
  bool _isLoading = false;
  String? _error;

  final _departureController = TextEditingController();
  final _arrivalController = TextEditingController();
  DateTime? _selectedMonth;
  String _nights = '';
  String _weekendDays = '0';

  Future<void> _handleSubmit() async {
    if (_departureController.text.isEmpty ||
        _arrivalController.text.isEmpty ||
        _selectedMonth == null ||
        _nights.isEmpty) {
        setState(() {
        _error = 'Per favore, compila tutti i campi richiesti';
        });
        return;
    }

    setState(() {
        _isLoading = true;
        _error = null;
    });

    try {
        String weekendRequirement;
        switch (_weekendDays) {
        case '0':
            weekendRequirement = 'none';
            break;
        case '1':
            weekendRequirement = 'one';
            break;
        case '2':
            weekendRequirement = 'both';
            break;
        default:
            weekendRequirement = 'none';
        }

        // Formatta la data nel modo corretto
        final selectedDate = _selectedMonth!;
        final departureMonth = '${selectedDate.year}-${selectedDate.month.toString().padLeft(2, '0')}';
        final params = {
        'departure_airport': _departureController.text,
        'arrival_airport': _arrivalController.text,
        'departure_month': departureMonth,
        'start_day': '1',
        'trip_duration': _nights,
        'weekend_requirement': weekendRequirement,
        };

        print('Sending parameters: $params');

        final result = await _apiService.searchFlights(params);
        
        print('Received response: $result');

        if (result['status'] == 'OK') {
        final flightResults = (result['results'][0] as List)
            .map((json) => FlightResult.fromJson(json))
            .toList();

        Navigator.push(
            context,
            MaterialPageRoute(
            builder: (context) => ResultsScreen(results: flightResults),
            ),
        );
        }

    } catch (e) {
        setState(() {
        _error = 'Errore durante la ricerca: $e';
        });
        ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Errore: $_error')),
        );
    } finally {
        setState(() {
        _isLoading = false;
        });
    }
    }

  Future<void> _selectMonth() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedMonth ?? DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
      initialDatePickerMode: DatePickerMode.year,
    );

    if (picked != null) {
      setState(() {
        _selectedMonth = DateTime(picked.year, picked.month, 1);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Colors.blue[50]!, Colors.blue[100]!],
              ),
            ),
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Card(
                  elevation: 8,
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          'Pianifica il tuo viaggio',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue[900],
                          ),
                        ),
                        const SizedBox(height: 32),
                        
                        TextField(
                          controller: _departureController,
                          decoration: const InputDecoration(
                            labelText: 'Aeroporto di partenza',
                            prefixIcon: Icon(Icons.flight_takeoff),
                            hintText: 'Es. Milano MXP',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),

                        TextField(
                          controller: _arrivalController,
                          decoration: const InputDecoration(
                            labelText: 'Aeroporto di arrivo',
                            prefixIcon: Icon(Icons.flight_land),
                            hintText: 'Es. Roma FCO',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),

                        InkWell(
                        onTap: () async {
                            showMonthPicker(
                            context: context,
                            initialDate: _selectedMonth ?? DateTime.now(),
                            firstDate: DateTime.now(),
                            lastDate: DateTime.now().add(const Duration(days: 365)),
                            ).then((date) {
                            if (date != null) {
                                setState(() {
                                _selectedMonth = date;
                                });
                            }
                            });
                        },
                        child: InputDecorator(
                            decoration: const InputDecoration(
                            labelText: 'Mese di partenza',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.calendar_today),
                            ),
                            child: Text(
                            _selectedMonth != null
                                ? DateFormat('MMMM yyyy', 'it_IT').format(_selectedMonth!)
                                : 'Seleziona un mese',
                            ),
                        ),
                        ),

                        TextField(
                          keyboardType: TextInputType.number,
                          onChanged: (value) => _nights = value,
                          decoration: const InputDecoration(
                            labelText: 'Numero di notti',
                            hintText: 'Es. 7',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),

                        DropdownButtonFormField<String>(
                          value: _weekendDays,
                          decoration: const InputDecoration(
                            labelText: 'Giorni del weekend richiesti',
                            border: OutlineInputBorder(),
                          ),
                          items: const [
                            DropdownMenuItem(value: '0', child: Text('Nessun giorno')),
                            DropdownMenuItem(value: '1', child: Text('1 giorno')),
                            DropdownMenuItem(value: '2', child: Text('2 giorni')),
                          ],
                          onChanged: (value) {
                            setState(() {
                              _weekendDays = value!;
                            });
                          },
                        ),
                        const SizedBox(height: 24),

                        ElevatedButton(
                          onPressed: _isLoading ? null : _handleSubmit,
                          style: ElevatedButton.styleFrom(
                            minimumSize: const Size(double.infinity, 50),
                          ),
                          child: _isLoading 
                            ? const CircularProgressIndicator(color: Colors.white)
                            : const Text('Cerca voli'),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
          if (_isLoading)
            Container(
              color: Colors.black.withOpacity(0.5),
              child: const Center(
                child: CircularProgressIndicator(),
              ),
            ),
        ],
      ),
    );
  }
}