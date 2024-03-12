<template>{{ timeSince }}</template>

<script>
export default {
    name: 'TimeSince',
    props: {
        date: {
            type: String,
            required: true,
        },
        suffix: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            now: Date.now(),
        };
    },
    computed: {
        dateTime() {
            return new Date(this.date);
        },
        timeSince() {
            const seconds = Math.floor((this.now - this.dateTime) / 1000);
            let interval = Math.floor(seconds / 31536000);
            let text = '';
            if (interval > 1) {
                text = `${interval} years`;
                return `${text}${this.suffix}`;
            }
            interval = Math.floor(seconds / 2592000);
            if (interval > 1) {
                text = `${interval} months`;
                return `${text}${this.suffix}`;
            }
            interval = Math.floor(seconds / 86400);
            if (interval > 1) {
                text = `${interval} days`;
                return `${text}${this.suffix}`;
            }
            interval = Math.floor(seconds / 3600);
            if (interval > 1) {
                text = `${interval} hours`;
                return `${text}${this.suffix}`;
            }
            interval = Math.floor(seconds / 60);
            if (interval > 1) {
                text = `${interval} minutes`;
            } else if (interval === 1) {
                text = `${interval} minute`;
            }
            if (text) {
                return `${text}${this.suffix}`;
            }
            return `just now`;
        },
    },
    created() {
        setInterval(() => {
            this.now = Date.now();
        }, 1000);
    },
    beforeUnmount() {
        clearInterval(this.now);
    },
};
</script>
