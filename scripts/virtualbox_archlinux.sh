#!/bin/bash

export LOGNAME=$(whoami)
export USER=$(whoami)

ISO_URL="https://mirror.rackspace.com/archlinux/iso/latest/archlinux-$(date +%Y.%m.)01-x86_64.iso"
ISO_FILE="archlinux-$(date +%Y.%m.)01-x86_64.iso"

if [ ! -d "${BUILD_DIR}" ]; then
    mkdir -p "${BUILD_DIR}"
fi

# :/Download the latest Arch Linux ISO

cd "${BUILD_DIR}"
if [ -f "${ISO_FILE}" ]; then
    echo "ISO file already exists: ${ISO_FILE}"
else
    echo "Downloading the latest Arch Linux ISO..."
    command curl -O "$ISO_URL"
fi

# :/Create the VirtualBox VM
echo "Creating VirtualBox VM: $VM_NAME"
VBoxManage createvm --name "$VM_NAME" --ostype "Linux_64" --register

# :/Configure VM settings
echo "Configuring VM settings..."
VBoxManage modifyvm "$VM_NAME" --memory 2048 --vram 128 --cpus 2 --nic1 nat

# :/Create a virtual disk
echo "Creating virtual disk..."
VBoxManage createhd --filename ~/VirtualBox\ VMs/"$VM_NAME"/"$VM_NAME".vdi --size 20000

# :/Attach the virtual disk to the VM
echo "Attaching virtual disk..."
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ~/VirtualBox\ VMs/"$VM_NAME"/"$VM_NAME".vdi
 
# :/Attach the Arch Linux ISO
echo "Attaching Arch Linux ISO..."
VBoxManage storagectl "$VM_NAME" --name "IDE Controller" --add ide
VBoxManage storageattach "$VM_NAME" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium "${BUILD_DIR}"/"$ISO_FILE"
 
# :/Start the VM
echo "Starting VM..."
VBoxManage startvm "$VM_NAME" --type gui

echo "VM $VM_NAME has been created and started."

