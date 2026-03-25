<template>
  <div class="space-y-3">
    <!-- Outbound -->
    <div class="rounded-xl bg-slate-800/60 p-4 space-y-2">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-sky-400 text-xs font-bold uppercase tracking-wider bg-sky-500/10 px-2 py-0.5 rounded-full">Outbound</span>
        <span class="text-slate-500 text-xs ml-auto">{{ flight.outbound.carrier }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.outbound.departure_time) }}</p>
          <p class="text-xs text-slate-400">{{ flight.outbound.departure_airport }}</p>
        </div>
        <div class="flex-1 flex flex-col items-center mx-3">
          <span class="text-xs text-slate-500 mb-1">{{ formatDuration(flight.outbound.duration) }}</span>
          <div class="w-full flex items-center gap-1">
            <div class="h-px flex-1 bg-slate-600"></div>
            <span class="text-slate-400 text-xs">✈</span>
            <div class="h-px flex-1 bg-slate-600"></div>
          </div>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.outbound.arrival_time) }}</p>
          <p class="text-xs text-slate-400">{{ flight.outbound.arrival_airport }}</p>
        </div>
      </div>
    </div>

    <!-- Return -->
    <div class="rounded-xl bg-slate-800/60 p-4 space-y-2">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-violet-400 text-xs font-bold uppercase tracking-wider bg-violet-500/10 px-2 py-0.5 rounded-full">Return</span>
        <span class="text-slate-500 text-xs ml-auto">{{ flight.inbound.carrier }}</span>
      </div>
      <div class="flex items-center justify-between text-sm">
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.inbound.departure_time) }}</p>
          <p class="text-xs text-slate-400">{{ flight.inbound.departure_airport }}</p>
        </div>
        <div class="flex-1 flex flex-col items-center mx-3">
          <span class="text-xs text-slate-500 mb-1">{{ formatDuration(flight.inbound.duration) }}</span>
          <div class="w-full flex items-center gap-1">
            <div class="h-px flex-1 bg-slate-600"></div>
            <span class="text-slate-400 text-xs">✈</span>
            <div class="h-px flex-1 bg-slate-600"></div>
          </div>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-white font-mono">{{ formatTime(flight.inbound.arrival_time) }}</p>
          <p class="text-xs text-slate-400">{{ flight.inbound.arrival_airport }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  flight: { type: Object, required: true }
})

function formatTime(datetimeStr) {
  if (!datetimeStr) return '--:--'
  // Expected format: "2025-06-10T06:30:00" or "06:30:00"
  const timePart = datetimeStr.includes('T') ? datetimeStr.split('T')[1] : datetimeStr
  return timePart.slice(0, 5)
}

function formatDuration(minutes) {
  if (!minutes && minutes !== 0) return '--'
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m > 0 ? `${h}h ${String(m).padStart(2, '0')}m` : `${h}h`
}
</script>
