<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <h3 class="text-form-header" style="text-align: center;">Create your company</h3>
            <div class="field">
                    <label class="label" style="color:white;">Name</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input is-primary" type="text" placeholder="Company's name" v-model="companyName" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-building"></i>
                      </span>
                    </div>
                    <div v-if="companyAvailability == true && companyName.length > 0" style="color: #00d1b2">The company name is available to register</div>
                    <div v-if="companyAvailability == false && companyName.length > 0" style="color: #e60c0c">The company name is not available</div>
            </div>
            <div class="field">
                <label class="label" style="color:white;">Select Continent</label>
                    <div class="control">
                        <div class="select is-primary">
                        <select v-model="continent">
                            <option>Asia</option>
                            <option>North America</option>
                            <option>South America</option>
                            <option>Oceania</option>
                            <option>Europe</option>
                            <option>Africa</option>
                        </select>
                        </div>
                    </div>
                    <div v-if="continentError == true" style="color: #e60c0c">Invalid continent name</div>
            </div>
            <div class="field">
                <div class="notification is-primary">
                    This is a <strong>beta</strong> version. Each company will receive $300 credits to get started. 
                    In <strong>alpha</strong> version, you will have to select plan and pay for the chosen price as credits to start
                </div>
            </div>
            <div class="field">
                <div v-if="msg.length > 0" style="color: #e60c0c">{{this.msg}}</div>
                </div>

            

            <div class="control">
                    <button class="button is-primary" @click.prevent="createCompany()">Submit</button>
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
            companyName: "",
            companyAvailability: false,
            msg: "",
            continent: "Asia",
            continentError: false,
        }
    },

    watch: {
        companyName: function() {
            this.debounceGetCompanyName()
        }
    },

    created() {
        this.debounceGetCompanyName = _.debounce(this.checkAvailableCompany, 50)
    },

    methods: {
        checkAvailableCompany() {
            let form = new FormData()
            form.append("companyName", this.companyName)
            axios.post('/company/hasavailablename/', form, { headers: {
                'Content-Type': 'multipart/form-data'
                }}).then(response=> {
                    let data = response.data
                    this.companyAvailability = data.available
            })
        },

        createCompany() {
            if(this.companyAvailability && this.continentError == false)
            {
                let form = new FormData()
                form.append('companyName', this.companyName)
                axios.post('/company/create/', form, {headers: {'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    this.msg = data.message
                    
                })
            }

        },

        checkValidContinent() {
            if(['asia', 'europe', 'south america', 'north america', 'oceania', 'africa'].includes(this.continent.toLowerCase())){
                this.continentError = false;
            } else{
                this.continentError = true;
            }
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

.text-form-header {
    text-align: center;
    text-transform:uppercase;
    font-weight: bold;
    font-size: 20px;
}
</style>