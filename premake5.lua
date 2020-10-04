newoption {
    trigger = "shared",
    description = "Build as shared lib",
}

newoption {
    trigger = "arch",
    description = "Build for the given architecture",
    value = "ARCH"
}

workspace "Lua"
    configurations { "Debug", "Release" }

    architecture(_OPTIONS.arch)

    filter { "action:vs*" }
        defines { "_CRT_SECURE_NO_WARNINGS" }

    filter { "Debug" }
        symbols "On"

    filter { "Release" }
        optimize "On"

    project "lualib"
        kind(iif(_OPTIONS.shared, "SharedLib", "StaticLib"))
        language "C"

        targetname "lua51"

        includedirs {
            "src"
        }

        files {
            "src/*.c",
            "src/*.def"
        }

        removefiles { "src/luac.c", "src/lua.c", "src/print.c" }

        filter { "kind:SharedLib", "action:vs*" }
            defines { "LUA_BUILD_AS_DLL" }

    project "luac"
        kind "ConsoleApp"

        includedirs {
            "src"
        }

        files {
            "src/*.c",
        }

        removefiles {
            "src/lua.c",
        }


    project "lua"
        kind "ConsoleApp"

        includedirs {
            "src"
        }

        links {
            "lualib"
        }

        files {
            "src/lua.c"
        }

        if _OPTIONS.shared then
            filter { "action:vs*" }
                defines { "LUA_BUILD_AS_DLL" }
        end
