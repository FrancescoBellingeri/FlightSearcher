<template>
  <div class="relative">
    <label class="block text-sm font-semibold text-slate-300 mb-1">{{ label }}</label>
    <div class="relative">
      <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">✈️</span>
      <input
        type="text"
        :id="id"
        v-model="query"
        @input="onInput"
        autocomplete="off"
        :placeholder="placeholder"
        class="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  placeholder: { type: String, default: 'Es. MXP' },
  id: { type: String, required: true },
})

const emit = defineEmits(['update:modelValue'])

const query = ref('')

watch(() => props.modelValue, (val) => {
  query.value = val ?? ''
}, { immediate: true })

function onInput() {
  emit('update:modelValue', query.value.toLowerCase().trim())
}
</script>
