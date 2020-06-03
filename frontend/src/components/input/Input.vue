<template>
  <div 
  :class="{ 'checkbox-input-container': type==='checkbox' }"
  >
    <label class="label">{{label}}</label>

    <select 
      v-if="type === 'select'" 
      :value="value" 
      @input="sendInput"
      :required="required"
      class="input"
     >
          <option
            v-for="(item) in options"
            :key="item.value"
            :value="item.value"
          >{{item.label}}</option>
     </select>

    <textarea 
      v-else-if="type === 'textarea'" 
      :value="value" 
      @input="sendInput"
      :required="required"
      class="input"
     ></textarea>
     <div 
      v-else-if="type === 'radio'"
      >

        <div 
        class="radio-input-container" 
        v-for="(item, index) in options"
        :key="index"
        >
          <input
            :value="item.value"
            @input="sendInput"
            type="radio"
            :required="required"
            :name="name"
            class="input"
          />
          <label class="label">{{item.label}}</label>
        </div>
      </div>
    <input
      v-else-if="type === 'checkbox'"
      class="input"
      :class="{ 'input--invalid': !valid }"
      :checked="!!value"
      @input="sendInput"
      :type="type"
      :required="required"
    />
    <input
      v-else
      class="input"
      :class="{ 'input--invalid': !valid }"
      :value="value"
      @input="sendInput"
      :type="type"
      :required="required"
    />
  </div>
</template>

<script>
export default {
  name: "Input",
  props: {
      valid: {
          type: Boolean,
          default: true
      }, 
      value: {
          type: [String, Boolean, Number]
      }, 
      type: {
          type: String
      }, 
      label: {
          type: String
      },
      required: {
            type: Boolean,
            default: false
      },
      name: {
          type: String,
      },
      errorMessage: {
          type: String,
          default: "Error"
      },
      options: {
        type: Array,
        default: () => []
      }
  },
  methods: {
      sendInput(event) {
        if (this.type === 'checkbox') {
          this.$emit('input', event.target.checked)
        } else {
          this.$emit('input', event.target.value)
        }
        this.$nextTick(() => event.target.setCustomValidity(!this.valid?this.errorMessage:''))
      }
  },
};
</script>

<style>
</style>