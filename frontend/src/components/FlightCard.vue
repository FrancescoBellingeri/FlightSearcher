<template>
  <div class="space-y-3">
    <!-- Andata -->
    <div class="rounded-xl bg-slate-800/60 p-4 space-y-2">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-sky-400 text-xs font-bold uppercase tracking-wider bg-sky-500/10 px-2 py-0.5 rounded-full">Andata</span>
        <span class="text-slate-500 text-xs ml-auto">{{ flight.andata['compagnia aerea'] }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.andata['orario partenza']) }}</p>
          <p class="text-xs text-slate-400">{{ departure }}</p>
        </div>
        <div class="flex-1 flex flex-col items-center mx-3">
          <span class="text-xs text-slate-500 mb-1">{{ flight.andata['durata volo'] }}h</span>
          <div class="w-full flex items-center gap-1">
            <div class="h-px flex-1 bg-slate-600"></div>
            <span class="text-slate-400 text-xs">✈</span>
            <div class="h-px flex-1 bg-slate-600"></div>
          </div>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.andata['orario arrivo']) }}</p>
          <p class="text-xs text-slate-400">{{ arrival }}</p>
        </div>
      </div>
    </div>

    <!-- Ritorno -->
    <div class="rounded-xl bg-slate-800/60 p-4 space-y-2">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-violet-400 text-xs font-bold uppercase tracking-wider bg-violet-500/10 px-2 py-0.5 rounded-full">Ritorno</span>
        <span class="text-slate-500 text-xs ml-auto">{{ flight.ritorno['compagnia aerea'] }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.ritorno['orario partenza']) }}</p>
          <p class="text-xs text-slate-400">{{ arrival }}</p>
        </div>
        <div class="flex-1 flex flex-col items-center mx-3">
          <span class="text-xs text-slate-500 mb-1">{{ flight.ritorno['durata volo'] }}h</span>
          <div class="w-full flex items-center gap-1">
            <div class="h-px flex-1 bg-slate-600"></div>
            <span class="text-slate-400 text-xs">✈</span>
            <div class="h-px flex-1 bg-slate-600"></div>
          </div>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.ritorno['orario arrivo']) }}</p>
          <p class="text-xs text-slate-400">{{ departure }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  flight: { type: Object, required: true },
  departure: { type: String, default: '' },
  arrival: { type: String, default: '' },
})

function formatTime(datetimeStr) {
  if (!datetimeStr) return '--:--'
  // Formato atteso: "2025-06-10T06:30:00" o "06:30:00"
  const timePart = datetimeStr.includes('T') ? datetimeStr.split('T')[1] : datetimeStr
  return timePart.slice(0, 5)
}
</script>
