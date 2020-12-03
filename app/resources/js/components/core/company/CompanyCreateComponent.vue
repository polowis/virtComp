<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <div class="field">
                    <label class="label">Name</label>
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
            msg: ""
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
            if(this.companyAvailability)
            {
                let form = new FormData()
                form.append('companyName', this.companyName)
                axios.post('/company/create/', form, {headers: {'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    this.msg = data.message
                    
                })
            }

        }

    }
}
</script>

<style scoped>
.form {
    margin:3% auto 0 auto;
    padding:30px;
    width:400px;
    height:auto;
    overflow:hidden;
    background:white;
    border-radius:10px;
}
</style>