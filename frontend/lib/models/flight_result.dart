class FlightResult {
  final SearchDate searchDate;
  final FlightDetail bestFlight;
  final FlightDetail cheapestFlight;

  FlightResult({
    required this.searchDate,
    required this.bestFlight,
    required this.cheapestFlight,
  });

  factory FlightResult.fromJson(Map<String, dynamic> json) {
    return FlightResult(
      searchDate: SearchDate.fromJson(json['search_date']),
      bestFlight: FlightDetail.fromJson(json['best_flight']),
      cheapestFlight: FlightDetail.fromJson(json['cheapest_flight']),
    );
  }
}

class SearchDate {
  final String departure;
  final String returnDate;

  SearchDate({required this.departure, required this.returnDate});

  factory SearchDate.fromJson(Map<String, dynamic> json) {
    return SearchDate(
      departure: json['departure'],
      returnDate: json['return'],
    );
  }
}

class FlightDetail {
  final FlightLeg andata;
  final FlightLeg ritorno;
  final int prezzo;

  FlightDetail({
    required this.andata,
    required this.ritorno,
    required this.prezzo,
  });

  factory FlightDetail.fromJson(Map<String, dynamic> json) {
    return FlightDetail(
      andata: FlightLeg.fromJson(json['andata']),
      ritorno: FlightLeg.fromJson(json['ritorno']),
      prezzo: json['prezzo'],
    );
  }
}

class FlightLeg {
  final String orarioPartenza;
  final String orarioArrivo;
  final int durataVolo;
  final String compagniaAerea;

  FlightLeg({
    required this.orarioPartenza,
    required this.orarioArrivo,
    required this.durataVolo,
    required this.compagniaAerea,
  });

  factory FlightLeg.fromJson(Map<String, dynamic> json) {
    return FlightLeg(
      orarioPartenza: json['orario partenza'],
      orarioArrivo: json['orario arrivo'],
      durataVolo: json['durata volo'],
      compagniaAerea: json['compagnia aerea'],
    );
  }
}