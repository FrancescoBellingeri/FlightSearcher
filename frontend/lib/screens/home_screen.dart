import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _departureController = TextEditingController();
  final _arrivalController = TextEditingController();
  DateTime? _selectedMonth;
  String _nights = '';
  String _weekendDays = '0';

  void _handleSubmit() {
    print({
      'departureAirport': _departureController.text,
      'arrivalAirport': _arrivalController.text,
      'selectedMonth': _selectedMonth?.toString(),
      'nights': _nights,
      'weekendDays': _weekendDays,
    });
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
      body: Container(
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
                      onTap: _selectMonth,
                      child: InputDecorator(
                        decoration: const InputDecoration(
                          labelText: 'Mese di partenza',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.calendar_today),
                        ),
                        child: Text(
                          _selectedMonth != null
                              ? DateFormat.yMMMM().format(_selectedMonth!)
                              : 'Seleziona un mese',
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),

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
                      onPressed: _handleSubmit,
                      style: ElevatedButton.styleFrom(
                        minimumSize: const Size(double.infinity, 50),
                      ),
                      child: const Text('Cerca voli'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}