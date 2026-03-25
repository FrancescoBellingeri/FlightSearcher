<template>
  <div class="min-h-screen bg-slate-950 text-white font-sans">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div class="max-w-5xl mx-auto px-6 py-4 flex items-center gap-3">
        <span class="text-2xl">✈️</span>
        <div>
          <h1 class="text-xl font-bold text-white tracking-tight">FlightSearcher</h1>
          <p class="text-xs text-slate-400">Powered by Kiwi.com</p>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 py-10 space-y-10">

      <!-- Search Card -->
      <section class="bg-slate-900 border border-slate-700 rounded-2xl p-8 shadow-2xl">
        <h2 class="text-2xl font-bold mb-1 text-white">🔍 Nuova Ricerca</h2>
        <p class="text-slate-400 text-sm mb-8">Compila i parametri e avvia la ricerca su tutti i voli disponibili nel mese.</p>

        <form @submit.prevent="startSearch" class="space-y-6">

          <!-- Aeroporti -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <AirportInput
              id="departure-airport"
              label="🛫 Aeroporto di Partenza"
              placeholder="Es. MXP — Milano Malpensa"
              v-model="form.departure_airport"
            />
            <AirportInput
              id="arrival-airport"
              label="🛬 Aeroporto di Arrivo"
              placeholder="Es. IST — Istanbul"
              v-model="form.arrival_airport"
            />
          </div>

          <!-- Mese, giorno inizio, durata -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Mese -->
            <div>
              <label for="departure-month" class="block text-sm font-semibold text-slate-300 mb-1">📅 Mese di Partenza</label>
              <input
                id="departure-month"
                type="month"
                v-model="form.departure_month"
                required
                class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
              />
              <p class="mt-1 text-xs text-slate-500">Formato: YYYY-MM</p>
            </div>

            <!-- Giorno inizio -->
            <div>
              <label for="start-day" class="block text-sm font-semibold text-slate-300 mb-1">📆 Giorno di Inizio Ricerca</label>
              <input
                id="start-day"
                type="number"
                v-model.number="form.start_day"
                min="1"
                max="31"
                required
                placeholder="Es. 1"
                class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
              />
              <p class="mt-1 text-xs text-slate-500">La ricerca partirà da questo giorno del mese</p>
            </div>

            <!-- Durata viaggio -->
            <div>
              <label for="trip-duration" class="block text-sm font-semibold text-slate-300 mb-1">⏱️ Durata del Viaggio (giorni)</label>
              <input
                id="trip-duration"
                type="number"
                v-model.number="form.trip_duration"
                min="1"
                required
                placeholder="Es. 7"
                class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
              />
              <p class="mt-1 text-xs text-slate-500">Numero di notti/giorni di permanenza</p>
            </div>
          </div>

          <!-- Weekend Requirement -->
          <div>
            <label class="block text-sm font-semibold text-slate-300 mb-3">🗓️ Requisiti Weekend</label>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <label
                v-for="opt in weekendOptions"
                :key="opt.value"
                :for="`weekend-${opt.value}`"
                :class="[
                  'flex flex-col items-center gap-1 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200',
                  form.weekend_requirement === opt.value
                    ? 'border-sky-500 bg-sky-500/10 text-sky-400'
                    : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-500'
                ]"
              >
                <input
                  :id="`weekend-${opt.value}`"
                  type="radio"
                  :value="opt.value"
                  v-model="form.weekend_requirement"
                  class="sr-only"
                />
                <span class="text-2xl">{{ opt.icon }}</span>
                <span class="text-sm font-semibold">{{ opt.label }}</span>
                <span class="text-xs text-center leading-tight opacity-70">{{ opt.desc }}</span>
              </label>
            </div>
          </div>

          <!-- Filtri avanzati -->
          <div class="border border-slate-700 rounded-xl p-5 space-y-5">
            <h3 class="text-sm font-semibold text-slate-300">⚙️ Filtri Avanzati</h3>

            <!-- Orari -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-xs font-semibold text-slate-400 mb-2">🛫 Orario partenza andata</label>
                <div class="flex items-center gap-2">
                  <input type="number" v-model.number="form.out_dep_from" min="0" max="23" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="Da (0)" />
                  <span class="text-slate-500 shrink-0">—</span>
                  <input type="number" v-model.number="form.out_dep_to" min="1" max="24" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="A (24)" />
                </div>
                <p class="mt-1 text-xs text-slate-500">Ore (0–24)</p>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-400 mb-2">🛬 Orario partenza ritorno</label>
                <div class="flex items-center gap-2">
                  <input type="number" v-model.number="form.ret_dep_from" min="0" max="23" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="Da (0)" />
                  <span class="text-slate-500 shrink-0">—</span>
                  <input type="number" v-model.number="form.ret_dep_to" min="1" max="24" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="A (24)" />
                </div>
                <p class="mt-1 text-xs text-slate-500">Ore (0–24)</p>
              </div>
            </div>

            <!-- Scali -->
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-2">🔀 Numero di scali</label>
              <div class="flex gap-3">
                <label
                  v-for="opt in stopOptions"
                  :key="opt.value"
                  :class="[
                    'flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border-2 cursor-pointer transition-all duration-200 text-center',
                    form.stop_number === opt.value
                      ? 'border-sky-500 bg-sky-500/10 text-sky-400'
                      : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-500'
                  ]"
                >
                  <input type="radio" :value="opt.value" v-model="form.stop_number" class="sr-only" />
                  <span class="text-lg">{{ opt.icon }}</span>
                  <span class="text-xs font-semibold">{{ opt.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="flex items-center gap-4 pt-2">
            <button
              type="submit"
              :disabled="loading"
              class="flex items-center gap-2 px-8 py-3 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-sky-500/25 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="animate-spin">⏳</span>
              <span v-else>🚀</span>
              {{ loading ? 'Ricerca in corso...' : 'Avvia Ricerca' }}
            </button>
            <span v-if="loading" class="text-sm text-slate-400 animate-pulse">
              La ricerca può richiedere diversi minuti…
            </span>
          </div>

        </form>
      </section>

      <!-- Error -->
      <div v-if="error" class="bg-red-950/50 border border-red-700 rounded-2xl p-6 flex items-start gap-4">
        <span class="text-2xl shrink-0">⚠️</span>
        <div>
          <p class="font-semibold text-red-400 mb-1">Errore durante la ricerca</p>
          <p class="text-sm text-red-300">{{ error }}</p>
        </div>
      </div>

      <!-- Results -->
      <section v-if="results.length > 0">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-white">📋 Risultati</h2>
            <p class="text-slate-400 text-sm mt-1">{{ results.length }} combinazioni trovate, ordinate per prezzo</p>
          </div>
          <span class="px-4 py-2 bg-emerald-600/20 border border-emerald-600/40 text-emerald-400 rounded-xl text-sm font-semibold">
            ✅ Ricerca completata
          </span>
        </div>

        <div class="space-y-4">
          <div
            v-for="(item, idx) in results"
            :key="idx"
            class="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden hover:border-slate-500 transition-all duration-200 group"
          >
            <!-- Header risultato -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-700/50 bg-slate-800/30">
              <div class="flex items-center gap-4">
                <span class="text-lg font-bold text-sky-400 bg-sky-500/10 border border-sky-500/30 rounded-lg px-3 py-1">#{{ idx + 1 }}</span>
                <div>
                  <p class="font-semibold text-white text-lg">
                    {{ formatDate(item.search_date.departure) }}
                    <span class="text-slate-400 font-normal mx-2">→</span>
                    {{ formatDate(item.search_date.return) }}
                  </p>
                  <p class="text-sm text-slate-400">{{ daysCount(item.search_date.departure, item.search_date.return) }} giorni di viaggio</p>
                </div>
              </div>
            </div>

            <!-- Voli -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-0 divide-y md:divide-y-0 md:divide-x divide-slate-700/50">
              <!-- Best -->
              <div class="p-6">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-yellow-400">⭐</span>
                  <span class="text-sm font-bold text-yellow-400 uppercase tracking-wide">Miglior Volo</span>
                  <span class="ml-auto text-xl font-bold text-white">€{{ item.best_flight.prezzo.toFixed(2) }}</span>
                </div>
                <FlightCard :flight="item.best_flight" :departure="form.departure_airport" :arrival="form.arrival_airport" />
              </div>
              <!-- Cheapest -->
              <div class="p-6">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-emerald-400">💰</span>
                  <span class="text-sm font-bold text-emerald-400 uppercase tracking-wide">Più Economico</span>
                  <span class="ml-auto text-xl font-bold text-white">€{{ item.cheapest_flight.prezzo.toFixed(2) }}</span>
                </div>
                <FlightCard :flight="item.cheapest_flight" :departure="form.departure_airport" :arrival="form.arrival_airport" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Empty state iniziale -->
      <div v-else-if="!loading && !error" class="text-center py-16 text-slate-600">
        <p class="text-5xl mb-4">🗺️</p>
        <p class="text-lg font-medium">Nessuna ricerca effettuata</p>
        <p class="text-sm mt-1">Compila il form sopra e premi "Avvia Ricerca"</p>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AirportInput from './components/AirportInput.vue'
import FlightCard from './components/FlightCard.vue'

const API_BASE = 'http://localhost:8000'

// Stato form
const form = reactive({
  departure_airport: '',
  arrival_airport: '',
  departure_month: new Date().toISOString().slice(0, 7),
  start_day: 1,
  trip_duration: 7,
  weekend_requirement: 'none',
  out_dep_from: null,
  out_dep_to: null,
  ret_dep_from: null,
  ret_dep_to: null,
  stop_number: null,
})

const stopOptions = [
  { value: null, icon: '🔀', label: 'Qualsiasi' },
  { value: 0,    icon: '✈️', label: 'Diretto' },
  { value: 1,    icon: '1️⃣', label: 'Max 1 scalo' },
  { value: 2,    icon: '2️⃣', label: 'Max 2 scali' },
]

const weekendOptions = [
  { value: 'none', icon: '❌', label: 'Nessuno', desc: 'Nessun requisito' },
  { value: 'one',  icon: '📅', label: 'Almeno 1', desc: 'Almeno un giorno nel weekend' },
  { value: 'both', icon: '📆', label: 'Almeno 2', desc: 'Almeno 2 giorni nel weekend' },
  { value: 'full', icon: '🗓️', label: 'Weekend Intero', desc: 'Sabato e domenica inclusi' },
]

const loading = ref(false)
const error = ref(null)
const results = ref([])

async function startSearch() {
  if (!form.departure_airport || !form.arrival_airport) {
    error.value = 'Inserisci sia l\'aeroporto di partenza che quello di arrivo.'
    return
  }

  loading.value = true
  error.value = null
  results.value = []

  try {
    const outFrom = form.out_dep_from ?? 0
    const outTo   = form.out_dep_to   ?? 24
    const retFrom = form.ret_dep_from ?? 0
    const retTo   = form.ret_dep_to   ?? 24
    const hasTimeFilter = form.out_dep_from !== null || form.out_dep_to !== null || form.ret_dep_from !== null || form.ret_dep_to !== null
    const times = hasTimeFilter ? `${outFrom}-${outTo}-0-24_${retFrom}-${retTo}-0-24` : null

    const response = await fetch(`${API_BASE}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        departure_airport: form.departure_airport,
        arrival_airport: form.arrival_airport,
        departure_month: form.departure_month,
        start_day: form.start_day,
        trip_duration: form.trip_duration,
        weekend_requirement: form.weekend_requirement,
        times,
        stop_number: form.stop_number,
      }),
    })

    const data = await response.json()

    if (data.status === 'OK') {
      results.value = data.results
      if (results.value.length === 0) {
        error.value = 'Nessun volo trovato per i parametri selezionati.'
      }
    } else {
      error.value = data.message || 'Errore sconosciuto dal backend.'
    }
  } catch (e) {
    error.value = `Impossibile connettersi al backend: ${e.message}`
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  const date = new Date(y, m - 1, d)
  return date.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
}

function daysCount(dep, ret) {
  const d1 = new Date(dep)
  const d2 = new Date(ret)
  return Math.round((d2 - d1) / (1000 * 60 * 60 * 24))
}
</script>