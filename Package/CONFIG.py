import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
src_lib_dir = ""
dst_lib_dir = ""
src_usr_lib_dir = ""
dst_lib_dir = ""
src_sbin_dir = ""
dst_sbin_dir = ""
src_usr_bin_dir = ""
dst_usr_bin_dir = ""
src_usr_sbin_dir = ""
dst_usr_sbin_dir = ""
src_include_dir = ""
dst_include_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global src_lib_dir
    global dst_lib_dir
    global src_usr_lib_dir
    global dst_lib_dir
    global src_usr_bin_dir
    global dst_usr_bin_dir
    global src_sbin_dir
    global dst_sbin_dir
    global src_usr_sbin_dir
    global dst_usr_sbin_dir
    global src_include_dir
    global dst_include_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    if arch == "armhf":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabihf")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabihf")
    elif arch == "armel":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabi")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabi")
    elif arch == "x86_64":
        src_lib_dir = iopc.getBaseRootFile("lib/x86_64-linux-gnu")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/x86_64-linux-gnu")
    else:
        sys.exit(1)
    dst_lib_dir = ops.path_join(output_dir, "lib")

    src_sbin_dir = iopc.getBaseRootFile("sbin")
    dst_sbin_dir = ops.path_join(output_dir, "sbin")

    src_usr_bin_dir = iopc.getBaseRootFile("usr/bin")
    dst_usr_bin_dir = ops.path_join(output_dir, "usr/bin")

    src_usr_sbin_dir = iopc.getBaseRootFile("usr/sbin")
    dst_usr_sbin_dir = ops.path_join(output_dir, "usr/sbin")

    src_include_dir = iopc.getBaseRootFile("usr/include/lxc")
    dst_include_dir = ops.path_join("include",args["pkg_name"])

def MAIN_ENV(args):
    set_global(args)
    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.mkdir(dst_sbin_dir)
    ops.copyto(ops.path_join(src_sbin_dir, "badblocks"), dst_sbin_dir)
    ops.copyto(ops.path_join(src_sbin_dir, "mke2fs"), dst_sbin_dir)
    ops.ln(dst_sbin_dir, "mke2fs", "mkfs.ext4")
    ops.copyto(ops.path_join(src_sbin_dir, "resize2fs"), dst_sbin_dir)
    ops.copyto(ops.path_join(src_sbin_dir, "tune2fs"), dst_sbin_dir)

    ops.mkdir(dst_lib_dir)

    lib_so = "libext2fs.so.2.4"
    ops.copyto(ops.path_join(src_lib_dir, lib_so), dst_lib_dir)
    ops.ln(dst_lib_dir, lib_so, "libext2fs.so.2")
    ops.ln(dst_lib_dir, lib_so, "libext2fs.so")

    lib_so = "libcom_err.so.2.1"
    ops.copyto(ops.path_join(src_lib_dir, lib_so), dst_lib_dir)
    ops.ln(dst_lib_dir, lib_so, "libcom_err.so.2")
    ops.ln(dst_lib_dir, lib_so, "libcom_err.so")

    lib_so = "libblkid.so.1.1.0"
    ops.copyto(ops.path_join(src_lib_dir, lib_so), dst_lib_dir)
    ops.ln(dst_lib_dir, lib_so, "libblkid.so.1.1")
    ops.ln(dst_lib_dir, lib_so, "libblkid.so.1")
    ops.ln(dst_lib_dir, lib_so, "libblkid.so")

    lib_so = "libuuid.so.1.3.0"
    ops.copyto(ops.path_join(src_lib_dir, lib_so), dst_lib_dir)
    ops.ln(dst_lib_dir, lib_so, "libuuid.so.1.3")
    ops.ln(dst_lib_dir, lib_so, "libuuid.so.1")
    ops.ln(dst_lib_dir, lib_so, "libuuid.so")

    lib_so = "libe2p.so.2.3"
    ops.copyto(ops.path_join(src_lib_dir, lib_so), dst_lib_dir)
    ops.ln(dst_lib_dir, lib_so, "libe2p.so.2")
    ops.ln(dst_lib_dir, lib_so, "libe2p.so")

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(output_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def MAIN_BUILD(args):
    set_global(args)
    return False

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_lib_dir, "."), "lib") 
    iopc.installBin(args["pkg_name"], ops.path_join(dst_sbin_dir, "."), "sbin") 
    #iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "."), dst_include_dir)
    return False

def MAIN_SDKENV(args):
    set_global(args)

    libs = ""
    libs += " -lext2fs -lcom_err -lblkid -luuid -le2p"
    iopc.add_libs(libs)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

