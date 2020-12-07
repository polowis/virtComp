<template>
    <div>
        <NavbarComponent></NavbarComponent>
            <div class="form">
            <h3 id="form-header">Log in</h3>
            <div class="field">
                    <label class="label" style="color:white;">Username</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="text" placeholder="Username" v-model="username" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <label class="label" style="color:white;">Password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" placeholder="" v-model="password" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-key"></i>
                      </span>
                    </div>
            </div>

            <div class="field" v-if="errorMessage.length > 0">
                <div class="notification is-danger">
                    <div>{{this.errorMessage}}</div>
                </div>
            </div>

            <div class="control">
                    <button class="button is-primary" @click.prevent="login()">Submit</button>
            </div>
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
            username: "",
            password: "",
            errorMessage: ""
        }
    },

    methods: {
        login() {
            let form = new FormData()
            form.append('username', this.username)
            form.append('password', this.password)
            axios.post('/login/', form, { 
                headers: {
                'Content-Type': 'multipart/form-data'
                }
          }).then(response => {
                let data = response.data
                if(data.status == 'success'){
                    window.location.href = data.redirect_url || '/home/'
                } else if(data.status == 'error') [
                    this.errorMessage = data.message
                ]
          })
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
            background:#738a75;
            border-radius:10px;
            color: #FFFFFF;
        }
        #form-header {
            text-align: center;
            text-transform:uppercase;
            font-weight: bold;
            font-size: 30px;
        }
    
</style>