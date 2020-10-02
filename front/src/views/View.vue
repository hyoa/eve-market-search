<template>
  <layout>
    <h1 class="text-4xl font-bold" v-if="filter">{{ filter.filter_name }}</h1>
    <section>
      <h1 @click="isCreationFormOpen = !isCreationFormOpen" class="text-3xl cursor-pointer">Update filter</h1>
      <filter-form 
        v-if="isCreationFormOpen && filter" 
        @form-submit=updateFilter
        :filterValue="filter"
        submitText="Update filter"
      />
    </section>
    <section class="mb-6">
      <h1 class="text-3xl">Report</h1>
      <div v-if="filter" class="text-gray-600 bg-white rounded-md px-4 py-2 my-4 shadow-md">
        <div>Buy price: {{ toCurrency(filter.min_buy_order) }} -> {{ toCurrency(filter.max_buy_order) }}</div>
        <div>Sell price: {{ toCurrency(filter.min_sell_order) }} -> {{ toCurrency(filter.max_sell_order) }}</div>
        <div>Volume: {{ filter.min_volume }} -> {{ filter.max_volume }}</div>
        <div>Taxe: {{ filter.buy_tax }} / {{ filter.sell_tax }} </div>
      </div>
      <table v-if="filter && filter.report" class="w-full bg-white rounded-md shadow-md">
        <tr>
          <th></th>
          <th class="text-left px-2">Name</th>
          <th class="text-right px-2">Buy Price</th>
          <th class="text-right px-2">Sell Price</th>
          <th class="text-right px-2">Volume</th>
          <th class="text-right px-2">Profit</th>
        </tr>
        <report-item
          v-for="reportItem of filter.report"
          :key="reportItem.type_id"
          :item="reportItem"
          extraClass="bg-gray-300 odd:bg-gray-200"
        />
      </table>
    </section>
  </layout>
</template>

<script>
import axios from 'axios'

import Layout from '../components/Layout.vue'
import FilterForm from '../components/FilterForm.vue'
import ReportItem from '../components/report/ReportItem.vue'

export default {
  components: { Layout, FilterForm, ReportItem },
  async created () {
    const res = await axios.get(`/.netlify/functions/viewFilter?id=${this.$route.params.id}`)

    this.filter = res.data

    if (this.filter.report) {
      this.filter.report = JSON.parse(this.filter.report)
    }
  },
  data () {
    return {
      filter: null,
      isCreationFormOpen: false
    }
  },
  methods: {
    async updateFilter (data) {
      const filterValues = { id: this.filter.id, ...data }

      await axios.post('/.netlify/functions/updateFilter', filterValues)
    },
    toCurrency (value) {
      return Number(value).toLocaleString('en')
    }
  }
}
</script>
