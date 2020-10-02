<template>
  <div class="border rounded-md p-4 shadow-md bg-white">
    <div class="flex justify-between justify-items-center items-center">
      <router-link
        :to="{ name: 'View', params: { id: this.id } }"
        class="text-xl font-semibold"
      >
        {{ name }}
      </router-link>
      <span @click="$emit('on-delete', this.id)" class="text-red-500">delete</span>
    </div>
    <div class="flex space-x-2">
      <div>
        {{ station }}
      </div>
      <div>
        {{ reportCount }}
      </div>
    </div>
    <div class="text-gray-500">
      Last updated at: xx/xx/xx
    </div>
  </div>
</template>

<script>
export default {
  props: ['name', 'station', 'report', 'id'],
  computed: {
    reportCount () {
      if (this.report) {
        return JSON.parse(this.report).length
      }

      return 0
    }
  }
}
</script>