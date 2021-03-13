<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <h3 class="text-form-header" style="text-align: center;">Construct your building</h3>
            <div class="field">
                <label class="label" style="color:white;">Select your building type</label>
                <div class="control">
                        <div class="select is-primary">
                        <select v-model="buildingType" v-on:change="fetchBuildingInfo">
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
                        <select v-model="method" v-if="landDetails.is_buy === true" v-on:change="fetchBuildingInfo">
                            <option>Buy</option>
                            <option>Rent</option>
                        </select>
                        <select v-model="method" v-if="landDetails.is_rent === true" v-on:change="fetchBuildingInfo">
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
                        <select v-model="level" v-if="method.toLowerCase() === 'rent'" v-on:change="fetchBuildingInfo">
                            <option v-for="level in 11" v-bind:key="level">{{level - 1}}</option>
                        </select>
                        <select v-else>
                            <option>0</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field" v-if="buildingInfo !== ''">
                <p>Cost: {{buildingInfo.cost}}</p>
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
            buildingType: "market",
            method: "rent",
            level: 0,
            buildingInfo: ""
        }
    },

    created() {
        this.fetchBuildingType()
        this.fetchLandDetails()
    },

    methods: {
        fetchBuildingType() {
            axios.get('/api/v1/constants/buildingtypename/').then(response => {
                let data = response.data
                this.supportedBuildingType = data
            })
        },

        fetchLandDetails() {
            let id = location.pathname.split("/")[2]
            axios.get(`/api/v1/landscape/${id}/view/`).then(response => {
                let data = response.data
                this.landDetails = data
            })
        },

        fetchBuildingInfo() {
            axios.get(`/api/v1/constants/buildinginfo/?building=${this.buildingType}&method=${this.method}&level=${this.level}`).then(response => {
                let data = response.data
                this.buildingInfo = data
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