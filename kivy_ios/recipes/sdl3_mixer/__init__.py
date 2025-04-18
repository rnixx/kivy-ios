import os

import sh

from kivy_ios.toolchain import Recipe, shprint


class LibSDL3MixerRecipe(Recipe):
    version = "78a2035cf4cf95066d7d9e6208e99507376409a7"
    # url = "https://github.com/libsdl-org/SDL_ttf/releases/download/release-{version}/SDL3_ttf-{version}.tar.gz"
    url = "https://github.com/libsdl-org/SDL_mixer/archive/{version}.tar.gz"
    embed_xcframeworks = ["SDL3_mixer"]
    include_dir = "include"
    pbx_frameworks = [
        "AudioToolbox",
        "CoreServices",
    ]

    def build_platform(self, plat):

        if plat.sdk == "iphonesimulator":
            destination = "generic/platform=iOS Simulator"
        else:
            destination = "generic/platform=iOS"

        shprint(
            sh.xcodebuild, "archive",
            "-scheme", "SDL3_mixer",
            "-project", "Xcode/SDL_mixer.xcodeproj",
            "-archivePath", f"Xcode/build/Release-{plat.sdk}",
            "-destination", destination,
            "-configuration", "Release",
            "BUILD_LIBRARY_FOR_DISTRIBUTION=YES",
            "SKIP_INSTALL=NO",
        )

    def lipoize_libraries(self):
        pass

    def create_xcframeworks(self):

        frameworks = []

        xcframework_dest = os.path.join(self.ctx.dist_dir, "xcframework", "SDL3_mixer.xcframework")
        if os.path.exists(xcframework_dest):
            # Delete the existing xcframework
            sh.rm("-rf", xcframework_dest)

        for plat in self.platforms_to_build:
            build_dir = self.get_build_dir(plat)
            frameworks.extend(
                [
                    "-framework",
                    os.path.join(
                        build_dir,
                        f"Xcode/build/Release-{plat.sdk}.xcarchive/Products/Library/Frameworks/SDL3_mixer.framework",
                    ),
                ]
            )

        shprint(
            sh.xcodebuild,
            "-create-xcframework",
            *frameworks,
            "-output",
            xcframework_dest,
        )


recipe = LibSDL3MixerRecipe()
