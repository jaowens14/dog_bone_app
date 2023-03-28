import os
def create_build_output_directory(build_number):
    # make location to store data ##########
    local_output_path = ".\\dog_bone_app_local_output\\"
    build_output_path = os.path.join(local_output_path, build_number)

    if os.path.exists(build_output_path):
        print("do nothing, build file already exists")
    else:
        os.makedirs(build_output_path)
    ########################################
    return build_output_path

