<template>
  <layout>
    <section id="create-filter">
      <h1 @click="isCreationFormOpen = !isCreationFormOpen" class="text-3xl cursor-pointer">Create filter</h1>
      <filter-form 
        v-if="isCreationFormOpen" 
        @form-submit=createFilter
        submitText="Create filter"
      />
    </section>
    <section id=list>
      <div>
        <h1 class="text-3xl">My filters</h1>
      </div>
      <ul>
        <li v-for="filter in filters" :key="filter.id" class="my-6">
          <list-item
            :name="filter.filter_name"
            :report="filter.report"
            :station="filter.location_id"
            :id="filter.id"
            :updateDate="filter.updated_at ? filter.updated_at : null"
            @on-delete="deleteFilter"
          />
        </li>
      </ul>
    </section>
  </layout>
</template>

<script>
import axios from 'axios'

import Layout from '../components/Layout.vue'
import FilterForm from '../components/FilterForm.vue'
import ListItem from '../components/ListItem.vue'

export default {
  components: { Layout, FilterForm, ListItem },
  async created () {
    await this.listFilters()
  },
  data () {
    return {
      isCreationFormOpen: false,
      filters: []
    }
  },
  methods: {
    async createFilter (filter) {
      await axios.post('/.netlify/functions/createFilter', filter)
    },
    async listFilters () {
      const res = await axios.get('/.netlify/functions/listFilters')
      this.filters = res.data
    },
    async deleteFilter (id) {
      await axios.get(`/.netlify/functions/deleteFilter?id=${id}`)
    }
  }
}
</script>
