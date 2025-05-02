import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/flight_result.dart';

class ResultsScreen extends StatelessWidget {
  final List<FlightResult> results;

  const ResultsScreen({Key? key, required this.results}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Risultati della ricerca'),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: results.length,
        itemBuilder: (context, index) {
          final result = results[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: ExpansionTile(
              title: Text(
                'Volo ${index + 1}: ${result.searchDate.departure} - ${result.searchDate.returnDate}',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text('Miglior prezzo: €${result.cheapestFlight.prezzo}'),
              children: [
                _buildFlightDetails('Miglior volo', result.bestFlight),
                const Divider(),
                _buildFlightDetails('Volo più economico', result.cheapestFlight),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildFlightDetails(String title, FlightDetail flight) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.blue,
            ),
          ),
          const SizedBox(height: 8),
          _buildLegDetails('Andata', flight.andata),
          const SizedBox(height: 8),
          _buildLegDetails('Ritorno', flight.ritorno),
          const SizedBox(height: 8),
          Text(
            'Prezzo totale: €${flight.prezzo}',
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegDetails(String title, FlightLeg leg) {
    final DateFormat timeFormat = DateFormat('HH:mm');
    final partenza = DateTime.parse(leg.orarioPartenza);
    final arrivo = DateTime.parse(leg.orarioArrivo);

    return Card(
      color: Colors.grey[100],
      child: Padding(
        padding: const EdgeInsets.all(8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Partenza: ${timeFormat.format(partenza)}'),
                    Text('Arrivo: ${timeFormat.format(arrivo)}'),
                  ],
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text('Durata: ${leg.durataVolo} min'),
                    Text(leg.compagniaAerea),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}