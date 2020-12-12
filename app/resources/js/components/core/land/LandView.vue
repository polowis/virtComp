<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="page">
            <div class="app-content">
                <div class="land-photo">
                    </div>
                <div class="land-details">
                    <div>Hello</div>
                </div>
            </div>

        </div>
    </div>
</template>
<script>
import NavbarComponent from '../../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

}
</script>

<style scoped>
.land-photo {
    width: 200px;
    float: left;
}

.land-details{
    width: 200px;
    float:right;
}
</style>