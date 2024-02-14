<template>
    <div>
        <input
            :id="my_id"
            v-model="my_value"
            type="range"
            :min="min"
            :max="max"
            class="slider"
        />
    </div>
</template>

<script>
import { v4 as uuid } from "uuid";

export default {
    name: "RangeSlider",
    props: {
        min: {
            type: Number,
            default: 0,
        },
        max: {
            type: Number,
            default: 100,
        },
        value: {
            type: Number,
            required: false,
            default: 50,
            validator: function () {
                return true;
            },
        },
    },
    emits: ["valueChanged"],
    data: function () {
        return {
            my_id: uuid(),
            my_value: null,
        };
    },
    watch: {
        my_value: function () {
            this.$emit("valueChanged", this.my_value);
        },
    },
    created: function () {
        this.my_value = this.value;
    },
    mounted: function () {},
    methods: {},
};
</script>

<style scoped></style>
