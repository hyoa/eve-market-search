<template>
  <div class="bg-gray-100 min-h-screen">
    <nav class="bg-blue-600 py-4 text-white">
      <div class="w-5/6 mx-auto">
        <router-link to="/">Home</router-link>
      </div>
    </nav>
    <div class="w-5/6 mx-auto">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Layout'
}
</script>

<style>

</style>