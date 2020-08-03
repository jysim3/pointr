<template>
  <div 
    :class="{ 'checkbox-input-container': type==='checkbox' }"
    class="form-group d-flex flex-wrap w-100"
  >
    <label class="label">{{ label }}</label>

    <select 
      v-if="type === 'select'" 
      :value="value" 
      :required="required"
      class="input"
      @input="sendInput"
    >
      <option
        v-for="(item) in options"
        :key="item.value"
        :disabled="disabled"
        :value="item.value"
      >
        {{ item.label }}
      </option>
    </select>

    <textarea 
      v-else-if="type === 'textarea'" 
      :value="value" 
      :name="name"
      :required="required"
      :disabled="disabled"
      class="input"
      @input="sendInput"
    />
    <div 
      v-else-if="type === 'radio'"
    >
      <div 
        v-for="(item, index) in options" 
        :key="index"
        class="radio-input-container"
      >
        <input
          :value="item.value"
          type="radio"
          :required="required"
          :disabled="disabled"
          :name="name"
          class="input"
          @input="sendInput"
        >
        <label class="label">{{ item.label }}</label>
      </div>
    </div>
    <input
      v-else-if="type === 'checkbox'"
      class="input"
      :class="{ 'input--invalid': !valid }"
      :checked="!!value"
      :type="type"
      :name="name"
      :disabled="disabled"
      :required="required"
      @input="sendInput"
    >
    <input
      v-else
      class="input"
      :class="{ 'input--invalid': !valid }"
      :value="value"
      :type="type"
      :name="name"
      :disabled="disabled"
      :required="required"
      @input="sendInput"
    >
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
    disabled: {
      type: Boolean,
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

<style scoped>
input[type='checkbox'] {
  width: auto;
  margin-left: 1rem;
}
.input {
  width: 100%;
}
</style>