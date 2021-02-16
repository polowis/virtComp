<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="page">
            <div class="app-content">
                <div class="land-photo">
                    <figure class="image">
                    <img src="/static/img/land.png" class="land-image">
                    </figure>
                    </div>
                <div class="land-details">
                    <h3>Land ID: {{land.land_id}}</h3>
                    
                    <p><b>Company Owner:</b> <b style="color: #ffeb3b">{{land.company_name}}</b></p>
                    <p v-if="land.company_name !== null" style="color: #f14668">Land Status: Not available to purchase </p>
                    <p v-else style="color: #00d1b2">Land Status: Available to purchase</p>
                    <p><b>Land Level:</b> {{land.level}}</p>
                    <p><b>Land Cost:</b> ${{land.buy_cost}}</p>
                    <p><b>Land Rent:</b> ${{land.rent_cost}} / week</p>
                    <p><b>Land Continent:</b> {{this.titleCase(land.continent)}}</p>
                    <p v-if="land.company_name === null" style="color: #00d1b2">Available to buy/rent</p>
                    <div v-if="land.company_name === null">
                        <div class="control" v-if="confirmedBuy == false && confirmedRent == false">
                            <button class="button is-primary" @click.prevent="confirmedBuy = true">Buy</button>
                            <button class="button is-primary" @click.prevent="confirmedRent = true">Rent</button>
                        </div>
                        <div class="control" v-if="confirmedBuy" >
                            <button class="button is-dark" @click.prevent="buyLand()">Confirm Buy</button>
                            <button class="button is-danger" @click.prevent="resetStatus()">Cancel</button>
                        </div>
                        <div class="control" v-if="confirmedRent" >
                            <button class="button is-dark" @click.prevent="rentLand()">Confirm Rent</button>
                            <button class="button is-danger" @click.prevent="resetStatus()">Cancel</button>
                        </div>
                    </div>
                    <p v-if="callbackError && callbackMessage.length > 0" style="color: #f14668; margin-top: 10px;">{{this.callbackMessage}}</p>
                    <p v-if="!callbackError && callbackMessage.length > 0" style="color: #00d1b2; margin-top: 10px;">{{this.callbackMessage}}</p>
                    <div v-if="land.owner == 1">
                        <p><b>Next rent due:</b> {{land.rent_due}}</p>
                        <div class="control" v-if="land.is_rent">
                            <button class="button is-dark">Pay rent</button>
                        </div>
                        <br>
                        <div class="control">
                            <button class="button is-success">Construct building</button>
                        </div>
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

    data() {
        return {
            land: "",
            confirmedBuy: false,
            confirmedRent: false,
            callbackMessage: "",
            callbackError: false
        }
    },

    mounted() {
        this.fetchLandDetail()
    },

    methods: {
        fetchLandDetail() {
            let id = location.pathname.split("/")[2]
            axios.get(`/api/v1/landscape/${id}/view/`).then(response => {
                let data = response.data
                this.land = data
            })
        },

        buyLand() {
            axios.post(`/land/${this.land.land_id}/buy/`).then(response => {
                let data = response.data
                this.callbackError = data.error
                this.callbackMessage = data.message
                this.fetchLandDetail()
            })
        },

        rentLand() {
            axios.post(`/land/${this.land.land_id}/rent/`).then(response => {
                let data = response.data
                this.callbackError = data.error
                this.callbackMessage = data.message
                this.fetchLandDetail()
            })
        },

        resetStatus() {
            this.callbackError = false
            this.callbackMessage = ""
            this.confirmedBuy = false
            this.confirmedRent = false
        },

        titleCase(str="asia") {
            let splitString = str.toLowerCase().split(' ');
            for (let i = 0; i < splitString.length; i++) {
               
                splitString[i] = splitString[i].charAt(0).toUpperCase() + splitString[i].substring(1);     
            }
            return splitString.join(' '); 
        },

    }

}
</script>

<style scoped>
.land-photo {
    width: 500px;
    float: left;
    margin-left: 20px;
}

.land-details{
    width: 500px;
    float:right;
    margin-right: 20px;
}
.land-image{
    width: 500px; 
    height: 300px
}
</style>