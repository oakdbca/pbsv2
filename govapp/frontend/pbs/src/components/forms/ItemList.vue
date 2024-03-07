<template>
    <ol class="list-group">
        <li
            class="list-group-item d-flex justify-content-between align-items-start"
        >
            <div class="ms-2 me-auto">
                <div class="fw-bold">
                    <a href="#">BPU000099</a>
                </div>
                An awesome burn plan unit name.
            </div>
            <BadgeStatus class="p-2" status="draft" />
        </li>

        <li
            class="list-group-item d-flex justify-content-between align-items-start"
        >
            <div class="ms-2 me-auto">
                <div class="fw-bold">
                    <a href="#">BPE004444</a>
                </div>
                A burn plan element that is truly wild.
            </div>
            <BadgeStatus
                class="p-2"
                status="with_district_manager"
                status-display="With District Manager"
            />
        </li>
        <li
            class="list-group-item d-flex justify-content-between align-items-start"
        >
            <div class="ms-2 me-auto">
                <div class="fw-bold">
                    <a href="#">AR000343</a>
                </div>
                Send a huge plane in full of water please!
            </div>
            <BadgeStatus
                class="p-2"
                status="with_regional_manager"
                status-display="With Regional Manager"
            />
        </li>
    </ol>
</template>

<script>
export default {
    name: 'ToastList',
};
</script>
