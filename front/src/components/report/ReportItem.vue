<template>
  <tr :class="extraClass" class="px-2">
    <td>
      <img :src="`https://images.evetech.net/types/${item.type_id}/icon`" alt="">
    </td>
    <td class="text-left px-2">{{ item.name }}</td>
    <td class="text-right px-2">{{ toCurrency(item.buy_order) }}</td>
    <td class="text-right px-2">{{ toCurrency(item.sell_order) }}</td>
    <td class="text-right px-2">{{ Math.round(item.volume) }}</td>
    <td class="text-right px-2">{{ Math.round(item.benefit_percent) }}%</td>
  </tr>
</template>

<script>
export default {
  props: ['item', 'extraClass'],
  methods: {
    toCurrency (value) {
      return Number(value).toLocaleString('en')
    }
  }
}
</script>