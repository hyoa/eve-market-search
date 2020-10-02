<template>
  <div>
    <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" v-if="label">{{ label }} </label>
    <input
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    >
  </div>

</template>

<script>
export default {
  props: ['type', 'placeholder', 'modelValue', 'label']
}
</script>