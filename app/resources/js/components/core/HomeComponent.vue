<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <h3 class="title center" style="padding-bottom: 10px;">Welcome back</h3>
        <p class="is-small center">VirtComp is a business simulation where you can earn rewards
            To get started, please create your company, you can create as many as you like but be smart. 
            To get assistance, please visit our <a href="/help">help page</a>
        </p>
        <div class="field center">
                <div class="notification is-primary">
                    This is beta version, each account can only create one company. In alpha version, you can spend money to create more than one company. 
                </div>
            </div>
        <div class="wrapper-table">
        <div style="width: 700px">
         <a class="button is-success is-small is-pulled-right">
                <span class="icon is-small">
                <i class="fas fa-plus"></i>
                </span>
                <span @click.prevent="createCompany()">Create a company</span>
        </a>
        </div>

        <table class="table is-hoverable" style="width: 700px">
            <thead>
                <th>Company Name</th>
                <th>Current Balance</th>
                <th>No. Cooperations</th>
                <th>No. Employees</th>
            </thead>
            <tbody>
                <tr v-for="company in companiesOwned" v-bind:key=company.company_id>
                    <td @click.prevent="registerSavedCompany(company.company_name)" style="cursor: pointer; color: #00d1b2">{{company.company_name}}</td>
                    <td>{{company.balance}}</td>
                    <td>0</td>
                    <td>0</td>
                </tr>
            </tbody>
        </table>
        </div>
    </div>
</template>
<script>
import NavbarComponent from '../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

    data() {
        return {
            companiesOwned: [],
            error: ""
        }
    },

    created() {
        this.fecthCurrentUserCompany()
    },

    methods: {
        createCompany() {
            window.location.href = "/company/create/"
        },

        fecthCurrentUserCompany() {
            axios.post('/user/companies/').then(response => {
                let data = response.data
                this.companiesOwned = data
            })
        },

        registerSavedCompany(name) {
            let company = name || ''
            if(company.length > 0){
                let form = new FormData()
                form.append("companyName", company)
                axios.post('/company/signed/', form, { headers: {
                    'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    if(data.hasOwnProperty('success')) {
                        window.location.href = data.redirect_url
                    } else{
                        this.error = 'Cannot securely open your company'
                    }
                })
            }
        }
    }
}
</script>
<style scoped>
    .center{
        margin: auto;
        padding: 10px 0px 30px 0px;
        width: 700px;
    }

    .wrapper-table {
        margin: auto;
        width: 700px;
    }

</style>