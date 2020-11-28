<template>
    <div>
        <NavbarComponent></NavbarComponent>
            <div class="form">
            <h3 id="form-header">Log in</h3>
            <div class="field">
                    <label class="label">Username</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="text" placeholder="Username" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <label class="label">Password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" placeholder="" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-key"></i>
                      </span>
                    </div>
            </div>

            <div class="control">
                    <button class="button is-primary">Submit</button>
            </div>
        </div>
    </div>
</template>
<script>
import NavbarComponent from '../NavbarComponent'
export default {
    components: {
        NavbarComponent
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
        #form-header {
            text-align: center;
            text-transform:uppercase;
            font-weight: bold;
            font-size: 30px;
        }
</style>