<template>
  <table style="width:100%">
    <tr>
      <th
        v-for="(n, i) in fields"
        :key="i"
      >
        {{ n }}
      </th>
    </tr>
    <tr 
      v-for="(event, index) in data" 
      :key="index" 
      :class="event._link ? 'link ' : ''"
      @click="clickRow(event)"
    >
      <td 
        v-for="(n, i) in fields"
        :key="i"
      >
        {{ event[n] }}
      </td>
    </tr>
  </table>
</template>
<script>
/*
requires 
field = ['names', 'of', 'the', 'data', 'key']
data = {
  'names': 'hello',
  'of' : 'hihi',
  ...

  }
*/
export default {
  name: "Table",
  props: {
    fields: {
      required: true,
      type: Array
    },
    data: {
      required: true,
      type: Array
    },
    actions: {
      default: () => [],
      type: Array
    }
  },
  methods: {
    clickRow(row) {
      this.$router.push(row._link)
    }
  }
}
</script>
<style scoped>

</style>