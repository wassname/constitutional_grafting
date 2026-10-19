-- Local Lua semantics and controlled textdraw fixtures only; no game/API validation. PI/OpenAI
print(_VERSION)
local text = "CONTACTS"
local ok, error_message = pcall(function() return text.match("CONTACTS") end)
assert(not ok)
assert(tostring(error_message):find("#2"), error_message)
assert(text:match("CONTACTS") == "CONTACTS")
assert(string.match(text, "CONTACTS") == "CONTACTS")
assert(not nil and not false)
print("PASS dot call lacks pattern argument #2; colon and explicit subject work; nil/false are both falsy")

local strings = {[2211] = "CONTACTS", [2219] = "~w~CONTACTS LIST"}
local function find_contact(first, last, stop_first, exact)
    local contactsId
    for id = first, last do
        local label = strings[id]
        if label and ((exact and label == "CONTACTS") or (not exact and label:find("CONTACTS", 1, true))) then
            contactsId = id
            if stop_first then break end
        end
    end
    return contactsId
end
assert(find_contact(2206, 2227, false, false) == 2219)
assert(find_contact(2206, 2227, true, false) == 2211)
assert(find_contact(2206, 2227, false, true) == 2211)
assert(find_contact(0, 2047, false, true) == nil)
print("PASS controlled fixture: last substring 2219, first substring/exact label 2211, zero-based 2048 scan misses both")

function sampTextdrawIsExists(id) return strings[id] ~= nil end
function sampTextdrawGetString(id) return assert(strings[id]) end
local actual_draft = assert(load(assert(arg[1]) .. "\nreturn contactsId"))
assert(actual_draft() == 2211)
strings[2211], strings[2219] = nil, nil
assert(actual_draft() == nil)
print("PASS actual displayed draft snippet against controlled fixture: first match and missing match")
print("Scope: language semantics and synthetic fixtures, not MoonLoader ID validity, real API integration, server behaviour or model benefit")
