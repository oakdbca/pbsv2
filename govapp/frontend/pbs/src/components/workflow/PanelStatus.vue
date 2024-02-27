<template>
    <div class="card-body border-bottom">
        <div class="input-group">
            <span id="basic-addon1" class="input-group-text">Status</span>
            <span
                id="basic-addon1"
                class="input-group-text text-capitalize"
                :class="[badgeTextClass, badgeBackgroundClass]"
                >{{ statusText }}
                <i v-if="iconClass" class="bi ps-2" :class="iconClass"></i
            ></span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PanelStatus',
    props: {
        status: {
            type: String,
            required: true,
        },
        statusDisplay: {
            type: String,
            required: false,
            default: null,
        },
        statusColorMap: {
            type: Object,
            required: false,
            default: () => ({
                draft: {
                    text: 'text-white',
                    background: 'bg-secondary',
                    icon: 'bi-pencil-square',
                },
                'with assessor': {
                    text: 'text-white',
                    background: 'bg-primary',
                    icon: 'bi-clipboard',
                },
                approved: {
                    text: 'text-white',
                    background: 'bg-success',
                    icon: 'bi-check2-square',
                },
                cancelled: {
                    text: 'text-white',
                    background: 'bg-danger',
                    icon: 'bi-x-square',
                },
                discarded: {
                    text: 'text-white',
                    background: 'bg-danger',
                    icon: 'bi-trash3',
                },
            }),
        },
    },
    computed: {
        badgeTextClass() {
            return this.statusColorMap[this.status]?.text;
        },
        badgeBackgroundClass() {
            return this.statusColorMap[this.status]?.background;
        },
        iconClass() {
            return this.statusColorMap[this.status]?.icon;
        },
        statusText() {
            return this.statusDisplay ? this.statusDisplay : this.status;
        },
    },
};
</script>
