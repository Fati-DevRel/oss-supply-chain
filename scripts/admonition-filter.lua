-- Pandoc Lua filter for Material for MkDocs admonitions
-- Converts !!! type "title" syntax to LaTeX tcolorbox environments

-- Map admonition types to LaTeX environment names
local admonition_types = {
  tip = "admonitiontip",
  info = "admonitioninfo",
  warning = "admonitionwarning",
  danger = "admonitiondanger",
  note = "admonitionnote",
  example = "admonitionexample",
  -- Aliases
  hint = "admonitiontip",
  important = "admonitionwarning",
  caution = "admonitionwarning",
  attention = "admonitionwarning",
  error = "admonitiondanger",
  failure = "admonitiondanger",
  bug = "admonitiondanger",
  abstract = "admonitioninfo",
  summary = "admonitioninfo",
  tldr = "admonitioninfo",
  question = "admonitioninfo",
  help = "admonitioninfo",
  faq = "admonitioninfo",
  quote = "admonitionnote",
  cite = "admonitionnote",
  success = "admonitiontip",
  check = "admonitiontip",
  done = "admonitiontip",
}

-- Parse admonition header: !!! type "title" or !!! type
-- Also handles "inline" and "inline end" modifiers
local function parse_admonition_header(text)
  -- Remove "inline" and "inline end" modifiers for parsing
  local clean_text = text:gsub('%s+inline%s+end', ' '):gsub('%s+inline', ' ')

  -- Pattern: !!! type "title" or !!! type 'title' or !!! type
  -- Handle both straight quotes and curly quotes (Pandoc converts " to "")
  local admon_type, title = clean_text:match('^!!!%s+(%w+)%s+"([^"]*)"')
  if not admon_type then
    -- Try curly double quotes (left " U+201C, right " U+201D)
    admon_type, title = clean_text:match('^!!!%s+(%w+)%s+\226\128\156([^\226]*)\226\128\157')
  end
  if not admon_type then
    admon_type, title = clean_text:match("^!!!%s+(%w+)%s+'([^']*)'")
  end
  if not admon_type then
    -- Try curly single quotes (left ' U+2018, right ' U+2019)
    admon_type, title = clean_text:match("^!!!%s+(%w+)%s+\226\128\152([^\226]*)\226\128\153")
  end
  if not admon_type then
    admon_type = clean_text:match('^!!!%s+(%w+)')
    title = nil
  end

  return admon_type, title
end

-- Escape special LaTeX characters in title
local function escape_latex(s)
  if not s then return nil end
  s = s:gsub('\\', '\\textbackslash{}')
  s = s:gsub('&', '\\&')
  s = s:gsub('%%', '\\%%')
  s = s:gsub('%$', '\\$')
  s = s:gsub('#', '\\#')
  s = s:gsub('_', '\\_')
  s = s:gsub('{', '\\{')
  s = s:gsub('}', '\\}')
  s = s:gsub('~', '\\textasciitilde{}')
  s = s:gsub('%^', '\\textasciicircum{}')
  return s
end

-- Convert Pandoc blocks to LaTeX string
local function blocks_to_latex(blocks)
  if #blocks == 0 then
    return ""
  end
  local doc = pandoc.Pandoc(blocks)
  local latex = pandoc.write(doc, 'latex')
  return latex
end

-- Convert a CodeBlock (indented content) to paragraph blocks
local function codeblock_to_blocks(cb)
  -- The CodeBlock text is the raw content - parse it as markdown
  local parsed = pandoc.read(cb.text, 'markdown')
  return parsed.blocks
end

-- Process a list of blocks looking for admonitions
function Blocks(blocks)
  local new_blocks = {}
  local i = 1

  while i <= #blocks do
    local block = blocks[i]
    local is_admonition = false
    local admon_type, title

    -- Check if this block starts an admonition
    if block.t == "Para" then
      local text = pandoc.utils.stringify(block)
      if text:match('^!!!') then
        admon_type, title = parse_admonition_header(text)
        if admon_type then
          is_admonition = true
        end
      end
    end

    if is_admonition then
      -- Collect content blocks (following indented content)
      local content_blocks = {}
      i = i + 1

      while i <= #blocks do
        local next_block = blocks[i]

        -- Check if next block is part of admonition content
        -- Pandoc parses 4-space indented content as CodeBlock
        if next_block.t == "CodeBlock" then
          -- CodeBlock contains the indented content as plain text
          -- Parse it as markdown to get proper formatting
          local parsed_blocks = codeblock_to_blocks(next_block)
          for _, b in ipairs(parsed_blocks) do
            table.insert(content_blocks, b)
          end
          i = i + 1
          break  -- Admonition content ends after the code block
        elseif next_block.t == "BlockQuote" then
          -- BlockQuote might also contain content in some cases
          for _, b in ipairs(next_block.content) do
            table.insert(content_blocks, b)
          end
          i = i + 1
          break
        elseif next_block.t == "Para" then
          local text = pandoc.utils.stringify(next_block)
          if text:match('^!!!') then
            -- Start of new admonition, stop here
            break
          else
            -- Unindented paragraph ends the admonition
            break
          end
        else
          -- Other block types end the admonition
          break
        end
      end

      -- Get LaTeX environment name
      local env_name = admonition_types[admon_type:lower()] or "admonitionnote"

      -- Build LaTeX output
      local latex_content = blocks_to_latex(content_blocks)

      -- Escape title for LaTeX
      local safe_title = escape_latex(title)

      local latex_output
      if safe_title and safe_title ~= "" then
        latex_output = string.format(
          "\\begin{%s}[%s]\n%s\\end{%s}",
          env_name, safe_title, latex_content, env_name
        )
      else
        latex_output = string.format(
          "\\begin{%s}\n%s\\end{%s}",
          env_name, latex_content, env_name
        )
      end

      table.insert(new_blocks, pandoc.RawBlock('latex', latex_output))
    else
      table.insert(new_blocks, block)
      i = i + 1
    end
  end

  return new_blocks
end

return {
  {Blocks = Blocks}
}
