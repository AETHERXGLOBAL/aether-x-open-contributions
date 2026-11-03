start_server {tags {stream aof needs:debug external:skip} overrides {appendonly yes appendfsync always auto-aof-rewrite-percentage 0}} {
    test {W07 zero-transfer claims survive AOF replay} {
        r XGROUP CREATE ax_w07_zero g 0 MKSTREAM
        assert_equal {} [r XCLAIM ax_w07_zero g cNoop 0 1-1]
        set reply [r XAUTOCLAIM ax_w07_zero g cAuto 0 0-0 COUNT 10]
        assert_equal 0-0 [lindex $reply 0]
        assert_equal {} [lindex $reply 1]

        set names [lsort [lmap c [r XINFO CONSUMERS ax_w07_zero g] {dict get $c name}]]
        assert_equal {cAuto cNoop} $names
        assert_equal 0 [lindex [r XPENDING ax_w07_zero g] 0]

        assert_equal OK [r DEBUG LOADAOF]

        set names [lsort [lmap c [r XINFO CONSUMERS ax_w07_zero g] {dict get $c name}]]
        assert_equal {cAuto cNoop} $names
        assert_equal 0 [lindex [r XPENDING ax_w07_zero g] 0]
    }

    test {W07 purge-only claimant survives AOF replay} {
        r XADD ax_w07_purge 1-1 f v1
        r XGROUP CREATE ax_w07_purge g 0
        r XREADGROUP GROUP g cOriginal COUNT 1 STREAMS ax_w07_purge >
        assert_equal 1 [r XDEL ax_w07_purge 1-1]
        assert_equal {} [r XCLAIM ax_w07_purge g cPurge 0 1-1]

        set names [lsort [lmap c [r XINFO CONSUMERS ax_w07_purge g] {dict get $c name}]]
        assert_equal {cOriginal cPurge} $names
        assert_equal 0 [lindex [r XPENDING ax_w07_purge g] 0]

        assert_equal OK [r DEBUG LOADAOF]

        set names [lsort [lmap c [r XINFO CONSUMERS ax_w07_purge g] {dict get $c name}]]
        assert_equal {cOriginal cPurge} $names
        assert_equal 0 [lindex [r XPENDING ax_w07_purge g] 0]
    }

    test {W07 real transfer control survives AOF replay} {
        r XADD ax_w07_transfer 1-1 f v1
        r XGROUP CREATE ax_w07_transfer g 0
        r XREADGROUP GROUP g cOriginal COUNT 1 STREAMS ax_w07_transfer >
        assert_equal 1 [llength [r XCLAIM ax_w07_transfer g cTransfer 0 1-1 JUSTID]]

        assert_equal OK [r DEBUG LOADAOF]

        set names [lsort [lmap c [r XINFO CONSUMERS ax_w07_transfer g] {dict get $c name}]]
        assert_equal {cOriginal cTransfer} $names
        assert_equal 1 [lindex [r XPENDING ax_w07_transfer g] 0]
    }
}
