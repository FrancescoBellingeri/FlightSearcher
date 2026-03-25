<template>
  <div :class="['relative', isOpen ? 'z-[60]' : 'z-30']" :id="'airport-container-' + id">
    <label class="block text-sm font-semibold text-slate-300 mb-1">{{ label }}</label>
    <div class="relative">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">✈️</span>
      <input
        type="text"
        :id="id"
        v-model="query"
        @input="onInput"
        @focus="onFocus"
        autocomplete="off"
        :placeholder="placeholder"
        class="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
      />
      <!-- Loading Spinner -->
      <span v-if="loading" class="absolute right-4 top-1/2 -translate-y-1/2 text-sky-400">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
      </span>

      <!-- Autocomplete Dropdown -->
      <div
        v-if="isOpen && results.length > 0"
        class="absolute left-0 right-0 mt-2 bg-slate-800 border border-slate-600 rounded-xl shadow-2xl overflow-hidden z-50"
      >
        <ul class="max-h-[300px] overflow-y-auto divide-y divide-slate-700/50">
          <li
            v-for="item in results"
            :key="item.value + item.type"
            @click="selectItem(item)"
            class="px-5 py-3.5 hover:bg-slate-700 cursor-pointer transition-all duration-150 flex items-center gap-4 text-slate-200 group border-l-4 border-transparent hover:border-sky-500"
            :class="item.type === 'city' ? 'bg-slate-800/30' : ''"
          >
            <!-- Icon -->
            <div class="flex-shrink-0 text-slate-400 group-hover:text-sky-400 transition-colors p-2 rounded-xl bg-slate-900/50 group-hover:bg-sky-500/10 shadow-inner">
              <!-- City SVG -->
              <svg v-if="item.type === 'city'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
              <!-- Plane SVG -->
              <svg v-else class="w-5 h-5 transform" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path></svg>
            </div>

            <!-- Text Content -->
            <div class="flex-1 min-w-0">
               <div v-if="item.type === 'city'" class="font-bold text-white truncate text-[15px] tracking-wide">{{ item.label }}</div>
               <div v-else class="flex flex-col">
                 <div class="font-bold text-white truncate text-[15px] tracking-wide">
                   <span v-if="item.iata" class="text-sky-400 mr-1.5">{{ item.iata }}</span>{{ item.city }} <span class="font-normal text-slate-300">- {{ item.airport.replace(' Intl', '') }}</span>
                 </div>
                 <div class="text-[11px] text-slate-400 truncate uppercase mt-0.5 tracking-wider font-semibold">{{ item.country }}</div>
               </div>
            </div>

            <!-- Right Icon (Plus) -->
            <div class="flex-shrink-0 text-slate-500 opacity-40 group-hover:opacity-100 group-hover:text-emerald-400 transition-all bg-black/20 group-hover:bg-emerald-500/10 p-1.5 rounded-full border border-slate-700/50 group-hover:border-emerald-500/30">
               <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  displayLabel: { type: String, default: '' },
  label: { type: String, required: true },
  placeholder: { type: String, default: 'e.g. MXP' },
  id: { type: String, required: true },
})

const emit = defineEmits(['update:modelValue', 'update:displayLabel'])

const query = ref('')
const results = ref([])
const isOpen = ref(false)
const loading = ref(false)
let debounceTimeout = null

// Close the dropdown when the user clicks outside
function closeDropdown(e) {
  const container = document.getElementById('airport-container-' + props.id)
  if (container && !container.contains(e.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdown)
})

// Handle external reset (e.g. form clear)
watch(() => props.modelValue, (val) => {
  if (!val) {
    query.value = ''
    emit('update:displayLabel', '')
  }
})

async function fetchAirports(q) {
  if (!q || q.length < 2) {
    results.value = []
    isOpen.value = false
    return
  }

  loading.value = true
  try {
    const res = await fetch(`http://localhost:8000/airports?q=${encodeURIComponent(q)}`)
    const data = await res.json()
    if (data.status === 'OK') {
      results.value = data.results
      isOpen.value = true
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function onInput() {
  isOpen.value = true
  // Reset the v-model until the user selects a valid option,
  // ensuring the backend always receives a validated slug.
  emit('update:modelValue', '')

  if (debounceTimeout) clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    fetchAirports(query.value)
  }, 300)
}

function onFocus() {
  if (results.value.length > 0) {
    isOpen.value = true
  }
}

function selectItem(item) {
  query.value = item.label  // Show the display label in the input
  emit('update:modelValue', item.value)  // Send the Kiwi slug to the form
  emit('update:displayLabel', item.type === 'city' ? item.city : item.iata)
  isOpen.value = false
}
</script>
