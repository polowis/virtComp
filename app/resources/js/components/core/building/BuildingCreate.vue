<template>
    <div>
        <NavbarComponent></NavbarComponent>
    </div>
</template>
<script>
import NavbarComponent from '../../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

    data(){
        return {
            supportedBuildingType: []
        }
    },

    created() {
        this.fetchBuildingType()
    },

    methods: {
        fetchBuildingType() {
            axios.get('api/v1/constants/buildingtypename/').then(response => {
                let data = response.data
                this.supportedBuildingType = data
            })
        }
    }

    
}
</script>