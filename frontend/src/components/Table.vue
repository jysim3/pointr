<template>
        <table style="width:100%">
          <tr>
            <th v-for="(n, i) in fields" :key="i">{{n}}</th>
          </tr>
          <tr 
          v-for="(event, index) in data" 
          :key="index" 
          @click="clickRow(event)"
          :class="event._link ? 'link ' : ''"
          >
                <td 
                v-for="(n, i) in fields"
                :key="i" >
                    {{ event[n] }}
                </td>
          </tr>
        </table> 
    
</template>
<script>
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
table 			      { 
  border-spacing: 1; 
  border-collapse: collapse; 
  background: transparent;
  border-radius:6px;
  overflow:hidden;
  max-width:800px; 
  width:100%;
  margin:0 auto;
  position:relative;
  
}
table td,th           { 
  padding-left:8px
}

table th        { 
  height:60px;
  background: var(--c-primary);
  font-size:16px;
  color: #e3f2fd;
}

table tr        { 
    height:48px; 
    border-bottom: 2px solid var(--c-secondary);
    transition: 0.2s;
    background: white;
}
table tr.link:hover{ 
    background: #e3f2fd;
    cursor: pointer;
    transform: translate(0, -2px);
    transition: 0.2s;
}
table tr:last-child  { 
  border:0; 
}

table td,th { 
  text-align:left;
}


</style>