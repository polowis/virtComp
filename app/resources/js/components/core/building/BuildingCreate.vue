<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <h3 class="text-form-header" style="text-align: center;">Construct your building</h3>
            <div class="field">
                <label class="label" style="color:white;">Select your building type</label>
                <div class="control">
                        <div class="select is-primary">
                        <select v-model="buildingType">
                            <option v-for="building in supportedBuildingType" v-bind:key=building.name>
                                {{building.name}}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label" style="color:white;">Select your method of acquiring</label>
                <div class="control">
                    <div class="select is-primary">
                        <select v-model="method">
                            <option>Buy</option>
                            <option>Rent</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label" style="color:white;">Select your building level</label>
                <p class="has-text-danger">You cannot select level of your choice if you decide to buy</p>
                <div class="control">
                    <div class="select is-primary">
                        <select v-if="method.toLowerCase() === 'rent'">
                            <option v-for="level in 10" v-bind:key="level">{{level}}</option>
                        </select>
                        <select v-else>
                            <option>1</option>
                        </select>
                    </div>
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

    data(){
        return {
            landDetails: "",
            supportedBuildingType: [],
            buildingType: "",
            method: "Buy",
        }
    },

    created() {
        this.fetchBuildingType()
    },

    methods: {
        fetchBuildingType() {
            axios.get('/api/v1/constants/buildingtypename/').then(response => {
                let data = response.data
                this.supportedBuildingType = data
            })
        }
    }

    
}
</script>

<style scoped>
.form {
    margin:3% auto 0 auto;
    padding:30px;
    width:500px;
    height:auto;
    overflow:hidden;
    background:#738a75;
    border-radius:10px;
    color: #FFFFFF;
}
</style>