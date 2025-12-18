import Lake
open Lake DSL

package «ksystems» {
  -- add package configuration options here
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «KMath» {
  -- add library configuration options here
}

@[default_target]
lean_lib «Crypto» {
  -- add library configuration options here
}
