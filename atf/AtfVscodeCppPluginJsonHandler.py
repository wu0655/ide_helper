import os
import sys

from common.FileType import VsCodeJsonConfig
from common.vscode_config.JsonHandler import JsonHandler


class AtfVscodeCppPluginJsonHandler(JsonHandler):
    target_json_file = VsCodeJsonConfig.CppPlugin
    make_log = ""

    define_list = []
    proj_name = ""

    def __init__(self, blt_dir, code_dir, path, log):
        super().__init__(blt_dir, code_dir, path)
        self.make_log = log

    def do_update(self):
        ret = False
        self.handle_proj_name()
        self.handle_make_log()
        if len(self.define_list) > 0:
            self.json_content['configurations'][0]['defines'] = self.define_list
            ret = True
        if len(self.proj_name) > 0:
            self.json_content['env']['myPlat'] = self.proj_name
            ret = True
        return ret

    """
    DEFINES = -DDEBUG=0 -DENABLE_BACKTRACE=0 -DFIP_EMMC_OFFSET=0x8ac00000 -DBL2_MAX_SIZE=0x40000 -DGICV3_SUPPORT_GIC600=0 -DGIC_ENABLE_V4_EXTN=0 -DGIC_EXT_INTID=0 -DXLAT_TABLES_LIB_V2=1 -DPLAT_s32g2= -DS32G_EMU=0 -DS32GEN1_DRAM_INLINE_ECC=1 -DBL2_EL3_STACK_ALIGNMENT=512 -DS32_USE_LINFLEX_IN_BL31=0 -DS32_HAS_HV=0 -DS32_SET_NEAREST_FREQ=0 -DEXT_APP_SIZE=0x100000 -DFIP_MAXIMUM_SIZE=0x300000 -DFIP_ROFFSET="(EXT_APP_SIZE + FIP_MAXIMUM_SIZE)" -DBL2_BASE=0x800A0000 -DS32_LINFLEX_MODULE=0 -DA57_ENABLE_NONCACHEABLE_LOAD_FWD=0 -DSKIP_A57_L1_FLUSH_PWR_DWN=0 -DA53_DISABLE_NON_TEMPORAL_HINT=1 -DA57_DISABLE_NON_TEMPORAL_HINT=1 -DWORKAROUND_CVE_2017_5715=1 -DWORKAROUND_CVE_2018_3639=1 -DDYNAMIC_WORKAROUND_CVE_2018_3639=0 -DNEOVERSE_Nx_EXTERNAL_LLC=0 -DERRATA_A9_794073=0 -DERRATA_A15_816470=0 -DERRATA_A15_827671=0 -DERRATA_A17_852421=0 -DERRATA_A17_852423=0 -DERRATA_A35_855472=0 -DERRATA_A53_819472=0 -DERRATA_A53_824069=0 -DERRATA_A53_826319=0 -DERRATA_A53_827319=0 -DERRATA_A53_835769=0 -DERRATA_A53_836870=1 -DERRATA_A53_843419=0 -DERRATA_A53_855873=1 -DERRATA_A53_1530924=1 -DERRATA_A55_768277=0 -DERRATA_A55_778703=0 -DERRATA_A55_798797=0 -DERRATA_A55_846532=0 -DERRATA_A55_903758=0 -DERRATA_A55_1221012=0 -DERRATA_A55_1530923=0 -DERRATA_A57_806969=0 -DERRATA_A57_813419=0 -DERRATA_A57_813420=0 -DERRATA_A57_814670=0 -DERRATA_A57_817169=0 -DERRATA_A57_826974=0 -DERRATA_A57_826977=0 -DERRATA_A57_828024=0 -DERRATA_A57_829520=0 -DERRATA_A57_833471=0 -DERRATA_A57_859972=0 -DERRATA_A57_1319537=0 -DERRATA_A72_859971=0 -DERRATA_A72_1319367=0 -DERRATA_A73_852427=0 -DERRATA_A73_855423=0 -DERRATA_A75_764081=0 -DERRATA_A75_790748=0 -DERRATA_A76_1073348=0 -DERRATA_A76_1130799=0 -DERRATA_A76_1220197=0 -DERRATA_A76_1257314=0 -DERRATA_A76_1262606=0 -DERRATA_A76_1262888=0 -DERRATA_A76_1275112=0 -DERRATA_A76_1286807=0 -DERRATA_A76_1791580=0 -DERRATA_A76_1165522=0 -DERRATA_A76_1868343=0 -DERRATA_A76_1946160=0 -DERRATA_A77_1508412=0 -DERRATA_A77_1925769=0 -DERRATA_A77_1946167=0 -DERRATA_A78_1688305=0 -DERRATA_A78_1941498=0 -DERRATA_A78_1951500=0 -DERRATA_N1_1043202=0 -DERRATA_N1_1073348=0 -DERRATA_N1_1130799=0 -DERRATA_N1_1165347=0 -DERRATA_N1_1207823=0 -DERRATA_N1_1220197=0 -DERRATA_N1_1257314=0 -DERRATA_N1_1262606=0 -DERRATA_N1_1262888=0 -DERRATA_N1_1275112=0 -DERRATA_N1_1315703=0 -DERRATA_N1_1542419=0 -DERRATA_N1_1868343=0 -DERRATA_N1_1946160=0 -DERRATA_DSU_798953=0 -DERRATA_DSU_936184=0 -DERRATA_S32_050481=1 -DERRATA_S32_050543=1 -DSTACK_PROTECTOR_ENABLED=0 -DCRASH_REPORTING=1 -DEL3_EXCEPTION_HANDLING=0 -DSDEI_SUPPORT=0 -DALLOW_RO_XLAT_TABLES=0 -DAMU_RESTRICT_COUNTERS=0 -DARM_ARCH_MAJOR=8 -DARM_ARCH_MINOR=0 -DARM_IO_IN_DTB=0 -DBL2_AT_EL3=1 -DBL2_INV_DCACHE=1 -DBL2_IN_XIP_MEM=0 -DCOLD_BOOT_SINGLE_CPU=0 -DCOT_DESC_IN_DTB=0 -DCTX_INCLUDE_AARCH32_REGS=1 -DCTX_INCLUDE_EL2_REGS=0 -DCTX_INCLUDE_FPREGS=0 -DCTX_INCLUDE_MTE_REGS=0 -DCTX_INCLUDE_NEVE_REGS=0 -DCTX_INCLUDE_PAUTH_REGS=0 -DDECRYPTION_SUPPORT_none -DDISABLE_MTPMU=0 -DEL3_EXCEPTION_HANDLING=0 -DENABLE_AMU=0 -DENABLE_ASSERTIONS=0 -DENABLE_BTI=0 -DENABLE_FEAT_RNG=$(if $(findstring rng,${arch-features}),1,0) -DENABLE_FEAT_SB=$(if $(findstring sb,${arch-features}),1,0) -DENABLE_MPAM_FOR_LOWER_ELS=0 -DENABLE_PAUTH=0 -DENABLE_PIE=0 -DENABLE_PMF=0 -DENABLE_PSCI_STAT=0 -DENABLE_RUNTIME_INSTRUMENTATION=0 -DENABLE_SPE_FOR_LOWER_ELS=1 -DENABLE_SVE_FOR_NS=1 -DENCRYPT_BL31=0 -DENCRYPT_BL32=0 -DERRATA_SPECULATIVE_AT=1 -DERROR_DEPRECATED=0 -DFAULT_INJECTION_SUPPORT=0 -DGICV2_G0_FOR_EL3=0 -DHANDLE_EA_EL3_FIRST=0 -DHW_ASSISTED_COHERENCY=0 -DLOG_LEVEL=40 -DMEASURED_BOOT=0 -DNS_TIMER_SWITCH=0 -DPL011_GENERIC_UART=0 -DPLAT_batman -DPROGRAMMABLE_RESET_ADDRESS=1 -DPSCI_EXTENDED_STATE_ID=0 -DRAS_EXTENSION=0 -DRAS_TRAP_LOWER_EL_ERR_ACCESS=0 -DRECLAIM_INIT_CODE=0 -DRESET_TO_BL31=0 -DSDEI_IN_FCONF=0 -DSEC_INT_DESC_IN_FCONF=0 -DSEPARATE_CODE_AND_RODATA=0 -DSEPARATE_NOBITS_REGION=0 -DSPD_none -DSPIN_ON_BL1_EXIT=0 -DSPMD_SPM_AT_SEL2=1 -DSPM_MM=0 -DTRNG_SUPPORT=0 -DTRUSTED_BOARD_BOOT=0 -DUSE_COHERENT_MEM=0 -DUSE_DEBUGFS=0 -DUSE_ROMLIB=0 -DUSE_SP804_TIMER=0 -DUSE_SPINLOCK_CAS=0 -DUSE_TBBR_DEFS=1 -DWARMBOOT_ENABLE_DCACHE_EARLY=0
    """

    def handle_make_log(self):
        if not os.path.isfile(self.make_log):
            return
        defines = ""
        with open(self.make_log, 'r') as f:
            for line in f.readlines():
                if line.startswith("DEFINES"):
                    defines = line[len("DEFINES"):len(line)]
                    break
        if len(defines) == 0:
            return
        print(defines)
        tmp = defines.strip().split(" ")
        remove_str = "-D"
        for line in tmp:
            if len(line.strip()) <= len(remove_str):
                continue
            strip_head_len = len(remove_str)
            item = line[strip_head_len:len(line)].strip()
            if item.endswith("="):
                item = item[0:-1]
            self.define_list.append(item)

    def handle_proj_name(self):
        if os.path.exists(self.blt_dir) and os.path.isdir(self.blt_dir):
            tmp = self.blt_dir.split(os.sep)
            if tmp[-1].strip() == 'release' or tmp[-1].strip() == 'debug':
                self.proj_name = tmp[-2].strip()


if __name__ == "__main__":
    print('input=' + str(sys.argv))
    if len(sys.argv) > 4:
        make_log = sys.argv[4]
    else:
        make_log = ""

    obj = AtfVscodeCppPluginJsonHandler(sys.argv[1], sys.argv[2], sys.argv[3], make_log)
    obj.do_handle()
