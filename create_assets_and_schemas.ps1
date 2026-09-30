$basePath = "c:\Users\erpri\OneDrive\Desktop\worksheet wonder"
$schemasPath = Join-Path $basePath "05_JSON_Schemas"
$illusPath = Join-Path $basePath "03_Illustration_Library"

# TASK 1: SVGs
$assets = @(
    @{ id="bear"; category="Animals"; name="Bear"; color="#8B4513"; shape='<circle cx="50" cy="50" r="35" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="30" cy="25" r="12" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><circle cx="70" cy="25" r="12" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><circle cx="40" cy="45" r="4" fill="#1E293B"/><circle cx="60" cy="45" r="4" fill="#1E293B"/><path d="M 45 60 Q 50 65 55 60" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>' },
    @{ id="ball"; category="Objects"; name="Ball"; color="#EF4444"; shape='<circle cx="50" cy="50" r="40" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 10 50 Q 50 10 90 50" fill="none" stroke="#1E293B" stroke-width="3.5"/><path d="M 10 50 Q 50 90 90 50" fill="none" stroke="#1E293B" stroke-width="3.5"/>' },
    @{ id="butterfly"; category="Animals"; name="Butterfly"; color="#3B82F6"; shape='<path d="M 50 20 L 50 80" stroke="#1E293B" stroke-width="8" stroke-linecap="round"/><path d="M 50 50 C 10 10 10 40 50 50 C 10 60 10 90 50 50 C 90 10 90 40 50 50 C 90 60 90 90 50 50" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>' },
    @{ id="bee"; category="Animals"; name="Bee"; color="#F59E0B"; shape='<ellipse cx="50" cy="50" rx="35" ry="25" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 25 25 Q 35 10 45 25 M 75 25 Q 65 10 55 25" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/><path d="M 35 25 L 35 75 M 50 25 L 50 75 M 65 25 L 65 75" stroke="#1E293B" stroke-width="3.5"/><circle cx="25" cy="45" r="3" fill="#1E293B"/>' },
    @{ id="bird"; category="Animals"; name="Bird"; color="#60A5FA"; shape='<ellipse cx="50" cy="50" rx="30" ry="25" fill="COLOR" stroke="#1E293B" stroke-width="3.5"/><path d="M 20 50 L 5 45 L 5 55 Z" fill="#F59E0B" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="35" cy="40" r="3" fill="#1E293B"/><path d="M 60 40 Q 80 20 90 40 Q 75 60 60 50 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>' },
    @{ id="boat"; category="Transport"; name="Boat"; color="#D97706"; shape='<path d="M 20 60 L 80 60 L 70 80 L 30 80 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><path d="M 50 60 L 50 15 L 80 50 Z" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>' },
    @{ id="book"; category="Objects"; name="Book"; color="#10B981"; shape='<rect x="20" y="20" width="60" height="60" rx="5" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><path d="M 30 20 L 30 80" stroke="#1E293B" stroke-width="3.5"/><path d="M 40 40 L 60 40 M 40 50 L 60 50 M 40 60 L 60 60" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>' },
    @{ id="bell"; category="Objects"; name="Bell"; color="#FBBF24"; shape='<path d="M 50 20 C 20 20 20 70 10 70 L 90 70 C 80 70 80 20 50 20 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="50" cy="70" r="10" fill="#1E293B"/><path d="M 45 15 A 5 5 0 1 1 55 15" fill="none" stroke="#1E293B" stroke-width="3.5" stroke-linecap="round"/>' },
    @{ id="bus"; category="Transport"; name="Bus"; color="#F59E0B"; shape='<rect x="10" y="30" width="80" height="40" rx="5" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/><circle cx="30" cy="70" r="10" fill="#1E293B"/><circle cx="70" cy="70" r="10" fill="#1E293B"/><rect x="20" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/><rect x="45" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/><rect x="70" y="40" width="15" height="15" rx="2" fill="#FFFFFF" stroke="#1E293B" stroke-width="3.5"/>' },
    @{ id="banana"; category="Food"; name="Banana"; color="#FBBF24"; shape='<path d="M 20 80 C 10 30 50 10 80 20 C 50 30 30 50 20 80 Z" fill="COLOR" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>' }
)

$svgTemplate = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{0}</svg>'

foreach ($a in $assets) {
    $dir = Join-Path $illusPath $a.category
    if (-Not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    
    # SVG
    $cShape = $a.shape -replace "COLOR", $a.color
    $svg = $svgTemplate -f $cShape
    Set-Content -Path (Join-Path $dir "$($a.name).svg") -Value $svg -Encoding UTF8
    
    # Outline
    $oShape = $a.shape -replace "COLOR", "#FFFFFF"
    $svgOut = $svgTemplate -f $oShape
    Set-Content -Path (Join-Path $dir "$($a.name)_outline.svg") -Value $svgOut -Encoding UTF8
    
    # Meta
    $meta = [ordered]@{
        "id" = "asset-$($a.id)"
        "name" = $a.name
        "category" = $a.category
        "keywords" = @($a.id, "letter b", "alphabet")
        "letter" = "B"
        "difficulty" = 1
        "recommendedAge" = @(4, 5, 6)
        "usage" = [ordered]@{
            "fullColor" = "$($a.name).svg"
            "outline" = "$($a.name)_outline.svg"
        }
        "tags" = @($a.id, "kindergarten", "noun")
    }
    $meta | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $dir "$($a.name).json") -Encoding UTF8
}

# TASK 2: Schemas
$vocabSchema = [ordered]@{
    "type" = "object"
    "required" = @("word", "syllables", "phonics", "imageId", "outlineImageId", "category", "difficulty", "keywords", "sentence", "emoji")
    "properties" = [ordered]@{
        "word" = @{ type="string" }
        "syllables" = @{ type="integer" }
        "phonics" = @{ type="string" }
        "imageId" = @{ type="string" }
        "outlineImageId" = @{ type="string" }
        "category" = @{ type="string" }
        "difficulty" = @{ type="integer" }
        "keywords" = @{ type="array"; items=@{ type="string" } }
        "sentence" = @{ type="string" }
        "emoji" = @{ type="string" }
    }
}

$alphaProps = [ordered]@{
    "letter" = @{ type="string" }
    "uppercase" = @{ type="string" }
    "lowercase" = @{ type="string" }
    "phonicsSound" = @{ type="string" }
    "formationSteps" = @{ type="array"; items=@{ type="string" } }
    "difficulty" = @{ type="integer" }
    "themeColor" = @{ type="string" }
    "heroWords" = @{ type="array"; items=@{ type="string" } }
    "vocabulary" = @{ type="array"; items=$vocabSchema }
    "backupWords" = @{ type="array"; items=$vocabSchema }
    "searchTags" = @{ type="array"; items=@{ type="string" } }
    "curriculumReferences" = @{ type="array"; items=@{ type="string" } }
    "teacherTips" = @{ type="string" }
    "parentTips" = @{ type="string" }
    "fineMotorObjective" = @{ type="string" }
    "phonicsObjective" = @{ type="string" }
}

$schemas = @{
    "alphabet" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; '$id'="https://worksheetwonder.com/schemas/alphabet.schema.json"; title="Alphabet Schema"; type="object"; required=@("letter", "uppercase", "lowercase", "phonicsSound", "formationSteps", "difficulty", "themeColor", "heroWords", "vocabulary", "backupWords", "searchTags", "curriculumReferences", "teacherTips", "parentTips", "fineMotorObjective", "phonicsObjective"); properties=$alphaProps; additionalProperties=$false }
    "illustration" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; '$id'="https://worksheetwonder.com/schemas/illustration.schema.json"; title="Illustration Meta Schema"; type="object"; required=@("id", "name", "category", "keywords", "usage", "tags"); properties=[ordered]@{id=@{type="string"}; name=@{type="string"}; category=@{type="string"}; keywords=@{type="array"; items=@{type="string"}}; letter=@{type="string"}; difficulty=@{type="integer"}; recommendedAge=@{type="array"; items=@{type="integer"}}; usage=[ordered]@{type="object"; required=@("fullColor", "outline"); properties=[ordered]@{fullColor=@{type="string"}; outline=@{type="string"}}}; tags=@{type="array"; items=@{type="string"}}}; additionalProperties=$false }
    "number" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Number Schema"; type="object"; required=@("number"); properties=[ordered]@{number=@{type="integer"}}; additionalProperties=$false }
    "shape" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Shape Schema"; type="object"; required=@("shape"); properties=[ordered]@{shape=@{type="string"}}; additionalProperties=$false }
    "colour" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Colour Schema"; type="object"; required=@("colour"); properties=[ordered]@{colour=@{type="string"}}; additionalProperties=$false }
    "animal" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Animal Schema"; type="object"; required=@("animal"); properties=[ordered]@{animal=@{type="string"}}; additionalProperties=$false }
    "phonics" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Phonics Schema"; type="object"; required=@("sound"); properties=[ordered]@{sound=@{type="string"}}; additionalProperties=$false }
    "sightword" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Sightword Schema"; type="object"; required=@("word"); properties=[ordered]@{word=@{type="string"}}; additionalProperties=$false }
    "cvc" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="CVC Schema"; type="object"; required=@("word"); properties=[ordered]@{word=@{type="string"}}; additionalProperties=$false }
    "theme" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Theme Schema"; type="object"; required=@("theme"); properties=[ordered]@{theme=@{type="string"}}; additionalProperties=$false }
    "worksheet" = [ordered]@{ '$schema'="http://json-schema.org/draft-07/schema#"; title="Worksheet Schema"; type="object"; required=@("id", "type", "payload"); properties=[ordered]@{id=@{type="string"}; type=@{type="string"}; payload=@{type="object"}}; additionalProperties=$false }
}

foreach ($key in $schemas.Keys) {
    $schemas[$key] | ConvertTo-Json -Depth 10 | Set-Content -Path (Join-Path $schemasPath "$key.schema.json") -Encoding UTF8
}
