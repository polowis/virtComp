<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <div class="field">
                    <label class="label">Name</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="text" placeholder="Company's name" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-building"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                <label class="label">Select business field</label>
                <div class="control">
                    <div class="select is-primary">
                    <select>
                        <option>Hi</option>
                    </select>
                    </div>
                </div>
            </div>

            <div class="control">
                    <button class="button is-primary">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
import NavbarComponent from '../../NavbarComponent'
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
</style>