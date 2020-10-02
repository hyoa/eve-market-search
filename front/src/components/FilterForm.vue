<template>
  <form @submit.prevent='buildFilter' class="bg-white border rounded-md p-4 shadow-md">
    <input-simple v-model="newFilter.name" type="text" placeholder="name" label="Filter name"/>

    <fieldset class="border p-2 mt-4">
      <legend class="bg-blue-500 text-white px-2 py-1">Price</legend>
      <div class="flex space-x-4">
        <input-simple v-model="newFilter.minBuyOrder" type="text" placeholder="0" label="Min buy order"/>
        <input-simple v-model="newFilter.maxBuyOrder" type="text" placeholder="0" label="Max buy order"/>
      </div>

      <div class="flex space-x-4">
        <input-simple v-model="newFilter.minSellOrder" type="text" placeholder="0" label="Min sell order"/>
        <input-simple v-model="newFilter.maxSellOrder" type="text" placeholder="0" label="Max sell order"/>
      </div>

    </fieldset>

    <fieldset class="border p-2 mt-4">
      <legend class="bg-blue-500 text-white px-2 py-1">Misc</legend>

      <div class="flex space-x-4">
        <input-simple v-model="newFilter.minVolume" type="text" placeholder="0" label="Min volume"/>
        <input-simple v-model="newFilter.maxVolume" type="text" placeholder="0" label="Max volume"/>
      </div>

      <div class="flex space-x-4">
        <input-simple v-model="newFilter.buyTax" type="text" placeholder="0" label="Buy taxes"/>
        <input-simple v-model="newFilter.sellTax" type="text" placeholder="0" label="Sell taxes"/>
      </div>

    </fieldset>


    <fieldset class="border p-2 mt-4 mb-4">
      <legend class="bg-blue-500 text-white px-2 py-1">Global data</legend>

      <div>
        <input-simple v-model="newFilter.region" type="text" placeholder="The Forge" label="Region"/>
      </div>

      <div>
        <input-simple v-model="newFilter.station" type="text" placeholder="Jita IV" label="Station"/>
      </div>

    </fieldset>

    <submit-simple :text="submitText" />
  </form>
</template>

<script>
import InputSimple from './form/InputSimple.vue'
import SubmitSimple from './form/SubmitSimple.vue'

export default {
  components: { InputSimple, SubmitSimple },
  props: ['filterValue', 'submitText'],
  created () {
    if (this.filterValue) {
      this.newFilter = {
        name: this.filterValue.filter_name,
        minBuyOrder: this.filterValue.min_buy_order,
        maxBuyOrder: this.filterValue.max_buy_order,
        minSellOrder: this.filterValue.min_sell_order,
        maxSellOrder: this.filterValue.max_sell_order,
        minVolume: this.filterValue.min_volume,
        maxVolume: this.filterValue.max_volume,
        buyTax: this.filterValue.buy_tax,
        sellTax: this.filterValue.sell_tax,
        region: this.filterValue.region_id,
        station: this.filterValue.location_id,
      }
    }
  },
  data () {
    return {
      newFilter: {
        name: '',
        minBuyOrder: null,
        maxBuyOrder: null,
        minSellOrder: null,
        maxSellOrder: null,
        minVolume: null,
        maxVolume: null,
        buyTax: null,
        sellTax: null,
        region: null,
        station: null
      }
    }
  },
  methods: {
    buildFilter () {
      const data = this.newFilter

      if (
        data.name === ''
        || data.buyTax === null
        || data.sellTax === null
        || data.region === null
        || data.station === null
        || isNaN(parseFloat(data.buyTax))
        || isNaN(parseFloat(data.sellTax))
        || isNaN(parseInt(data.region))
        || isNaN(parseInt(data.station))
      ) {
        return
      }

      const filter = {
        filter_name: data.name,
        buy_tax: parseFloat(data.buyTax),
        sell_tax: parseFloat(data.sellTax),
        region_id: parseInt(data.region),
        location_id: parseInt(data.station),
        ...this.replaceFilterValues(data)
      }

      this.$emit('form-submit', filter)
    },
    replaceFilterValues (data) {
      return {
        min_buy_order: data.minBuyOrder === null ? 0 : parseInt(data.minBuyOrder),
        max_buy_order: data.maxBuyOrder === null ? 0 : parseInt(data.maxBuyOrder),
        min_sell_order: data.minSellOrder === null ? 0 : parseInt(data.minSellOrder),
        max_sell_order: data.maxSellOrder === null ? 0 : parseInt(data.maxSellOrder),
        min_volume: data.minVolume === null ? 0 : parseInt(data.minVolume),
        max_volume: data.maxVolume === null ? 0 : parseInt(data.maxVolume),
      }
    }
  }
}
</script>