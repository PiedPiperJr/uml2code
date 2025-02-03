import subprocess
from typing import Dict


def create_spring_boot_project(spring_data: Dict[str, str], output_dir: str) -> bool:
    command = [
        'spring',
        'init',
        '--build=maven',
        f"--group-id={spring_data['groupId']}",
        f"--artifact-id={spring_data['artifactId']}",
        f"--name={spring_data['name']}",
        f"--package-name={spring_data['packageName']}",
        f"--packaging={spring_data['packaging']}",
        f"--java-version={spring_data['javaVersion']}",
        f"--description={spring_data['description']}",
        f"--dependencies={spring_data['dependencies']}",
        output_dir
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, shell=True)
        print("Output:", result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating Spring project: {e.stderr}")
        return False
    
    except FileNotFoundError:
        print("Error: Spring CLI is not installed or not in PATH")
        return False