# Validation Framework

## Validation Registry

- [Source](https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/pxr/usd/usd/validationRegistry.h)

### Purpose

 UsdValidationRegistry manages and provides access to UsdValidator / UsdValidatorSuite for USD Validation.

### Description

UsdValidationRegistry is a singleton class, which serves as a central
registry to hold / own all validators and validatorSuites by their names.
Both Core USD and client-provided validators are registered with the
registry. Validators can be registered and retrieved dynamically, supporting
complex validation scenarios across different modules or plugins.

As discussed in UsdValidator, validators are associated with
UsdValidateLayerTaskFn, UsdValidateStageTaskFn or UsdValidatePrimTaskFn,
which govern how a layer, stage or a prim needs to be validated.
UsdValidator / UsdValidatorSuite also have metadata, which can either be
provided in the plugInfo.json when registering the validators via plugin
mechanism, or by providing metadata field when registering validators.

### Usage

Clients of USD can register validators either via plugin infrastructure,
which results in lazy loading of the validators, or explicitly register
validators in their code via appropriate APIs.

UsdValidator or UsdValidatorSuite can be registered using
specific metadata or names, and retrieved by their name. The registry also
provides functionality to check the existence of a validator / suite, load
validators / suites dynamically if they are not in the registry.

Clients can also retrieve metadata for validators associated with a
specific plugin, keywords or schemaTypes, this can help clients filter out
relevant validators they need to validate their context / scene.

Note that this class is designed to be thread-safe:
Querying of validator metadata, registering new validator (hence mutating
the registry) or retrieving previously registered validator are designed to
be thread-safe.

#### Example Registration with plugInfo.json

Example of registering a validator named "StageMetadataValidator" with 
doc metadata using plugInfo.json:
```
{
    "Plugins": [
    {
        "Info": {
            "Name": "usd"
            "LibraryPath": "@PLUG_INFO_LIBRARY_PATH",
            ....
            ....
            ....
            "Validators": {
                "keywords" : ["UsdCoreValidators"],
                ...
                "StageMetadataValidator": {
                    "doc": "Validates stage metadata."
                },
                ...
                ...
                ...
            }
        }
    } ]
}
```

The above example can then be registered in the plugin:

```
TF_REGISTRY_FUNCTION(UsdValidationRegistry)
{
    UsdValidationRegistry& registry = UsdValidationRegistry::GetInstance();
    const TfToken validatorName("usd:StageMetadataValidator");
    const UsdValidateStageTaskFn stageTaskFn = 
        [](const UsdStagePtr &usdStage) {
            UsdValidationErrorVector errors;
            if (!usdStage->GetDefaultPrim()) {
                errors.emplace_back(UsdValidationErrorType::Error,
                    {UsdValidationErrorSite(usdStage, SdfPath("/"))}, 
                    "Stage has missing or invalid defaultPrim.");
            }
            if (!usdStage->HasAuthoredMetadata(
                    UsdGeomTokens->metersPerUnit)) {
                errors.emplace_back(UsdValidationErrorType::Error,
                    {UsdValidationErrorSite(usdStage, SdfPath("/"))},
                    "Stage does not specify its linear scale in "
                    "metersPerUnit.");
            }
            if (!usdStage->HasAuthoredMetadata(
                    UsdGeomTokens->upAxis)) {
                errors.emplace_back(UsdValidationErrorType::Error,
                    {UsdValidationErrorSite(usdStage, SdfPath("/"))},
                    "Stage does not specify an upAxis.");
            }
            return errors;
        };
    registry.RegisterValidator(validatorName, stageTaskFn);
}
```

#### Example Registration explicitly in code

Clients can also register validators by explicitly providing
UsdValidatorMetadata, instead of relying on plugInfo.json for the same.
Though its recommended to use appropriate APIs when validator metadata is
being provided in the plugInfo.json.
Example of validator registration by explicitly providing metadata, when its
not available in the plugInfo.json:

```
{
    UsdValidationRegistry& registry = UsdValidationRegistry::GetInstance();
    const UsdValidatorMetadata &metadata = GetMetadataToBeRegistered();
    const UsdValidateLayerTaskFn &layerTask = GetLayerTaskForValidator();
    registry.RegisterValidator(metadata, layerTask);
}
```




## USD Validator Metadata
- [Source](https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/pxr/usd/usd/validator.h)

### Purpose

A structure which describes metadata for a UsdValidator.

### Description

The metadata values are populated from the plugInfo.json associated with a
validator's plugin. PlugInfo can provide the following validator metadata:

- name: A required field. This metadatum stores the validator name. For
validators defined in a plugin, the name must be a fully qualified name 
which includes the pluginName as well, separated by ":". This ensures,
plugin provided validator names are guaranteed to be unique.
- pluginPtr: Pointer to the plugin where a plugin based validator is defined.
nullptr for a non-plugin based validator.
- keywords: Keywords associated with this validator. 
- doc: Doc string explaining the purpose of the validator. 
- schemaTypes: If the validator is associated with specific schemaTypes.
- isSuite: If the validator represents a suite of validators.

## Usd Validator Suite

### Purpose
UsdValidatorSuite acts like a suite for a collection of tests, which
clients can use to bundle all tests relevant to test their concepts.

### Usage
If client failed to provide isSuite metadata for a UsdValidatorSuite
instance then the validatorSuite will not be registered, and client will
appropriately be warned.


## Writing a Validator - recommended practices

- Keyword metadata for a validator belonging to a schemaDomain should be: <SchemaDomain>Validators
    - Example: UsdCoreValidators, UsdShadeValidators
- Prefix plugin based validators with plugin name
    - Example: "usd:CompositionErrorTest", "usdShade:ShaderSdrCompliance"
- Provide public tokens for validator name and keyword metadata
    - Example: [usd](https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/pxr/usd/usd/validatorTokens.h)
    - Example: [usdShade](https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/pxr/usd/usdShade/validatorTokens.h)
- Logicial encapsulation of Validator rules
    - Each validator should represent a specific domain, not multiple domains
- Granular validation rules using PrimValidateTask vs StageValidateTask
    - Prefer lower level validation rules, if you only need to validate at the prim level, use a PrimValidateTask



## Writing a Validator - Example

Below is an example of adding a Validator for usdGeom to check for required stage metadata

### Add Validator Tokens

#### validatorTokens.cpp

```
#include "pxr/usd/usdGeom/validatorTokens.h"

PXR_NAMESPACE_OPEN_SCOPE

    TF_DEFINE_PUBLIC_TOKENS(UsdGeomValidatorNameTokens, USDGEOM_VALIDATOR_NAMES_TOKENS);
    TF_DEFINE_PUBLIC_TOKENS(UsdGeomValidatorKeywordTokens,
                            USDGEOM_VALIDATOR_KEYWORD_TOKENS);

PXR_NAMESPACE_CLOSE_SCOPE
```


#### validatorTokens.h

```

#ifndef USDGEOM_VALIDATOR_TOKENS_H
#define USDGEOM_VALIDATOR_TOKENS_H

/// \file

#include "pxr/pxr.h"
#include "pxr/usd/usdGeom/api.h"
#include "pxr/base/tf/staticTokens.h"

PXR_NAMESPACE_OPEN_SCOPE

#define USD_GEOM_VALIDATOR_NAME_TOKENS                   \
    ((usdGeomStageMetadataChecker, "usdGeom:StageMetadataChecker"))

#define USD_GEOM_VALIDATOR_KEYWORD_TOKENS                \
    (UsdGeomValidators)

///\def
/// Tokens representing validator names. Note that for plugin provided
/// validators, the names must be prefixed by usdGeom:, which is the name of
/// the usdGeom plugin.
    TF_DECLARE_PUBLIC_TOKENS(UsdGeomValidatorNameTokens, USDGEOM_API,
                             USD_GEOM_VALIDATOR_NAME_TOKENS);

///\def
/// Tokens representing keywords associated with any validator in the usdGeom
/// plugin. Clients can use this to inspect validators contained within a
/// specific keywords, or use these to be added as keywords to any new
/// validator.
    TF_DECLARE_PUBLIC_TOKENS(UsdGeomValidatorKeywordTokens, USDGEOM_API,
                             USD_GEOM_VALIDATOR_KEYWORD_TOKENS);

PXR_NAMESPACE_CLOSE_SCOPE

#endif
```


### Add Validator Class

```
#include "pxr/usd/usd/validationError.h"
#include "pxr/usd/usd/validationRegistry.h"
#include "pxr/usd/usdGeom/validatorTokens.h"
#include "pxr/usd/usdGeom/tokens.h"
#include "pxr/usd/usd/validator.h"

PXR_NAMESPACE_OPEN_SCOPE

    static
    UsdValidationErrorVector
    _GetStageMetadataErrors(const UsdStagePtr &usdStage)
    {
        UsdValidationErrorVector errors;
        if (!usdStage->HasAuthoredMetadata(
                UsdGeomTokens->metersPerUnit)) {
            errors.emplace_back(UsdValidationErrorType::Error,
                                UsdValidationErrorSites{UsdValidationErrorSite(usdStage, SdfPath("/"))},
                                "Stage does not specify its linear scale in "
                                "metersPerUnit.");
        }
        if (!usdStage->HasAuthoredMetadata(
                UsdGeomTokens->upAxis)) {
            errors.emplace_back(UsdValidationErrorType::Error,
                                UsdValidationErrorSites{UsdValidationErrorSite(usdStage, SdfPath("/"))},
                                "Stage does not specify an upAxis.");
        }

        return errors;
    }

    TF_REGISTRY_FUNCTION(UsdValidationRegistry)
    {
        UsdValidationRegistry &registry = UsdValidationRegistry::GetInstance();
        registry.RegisterPluginValidator(
                UsdGeomValidatorNameTokens->stageMetadataChecker, _GetStageMetadataErrors);
    }

PXR_NAMESPACE_CLOSE_SCOPE
```

### Add Unit Tests

```
#include "pxr/usd/usd/validator.h"
#include "pxr/usd/usd/validationError.h"
#include "pxr/usd/usdGeom/validatorTokens.h"
#include "pxr/usd/usd/validationRegistry.h"

#include <iostream>

PXR_NAMESPACE_USING_DIRECTIVE

static
void TestUsdStageMetadata()
{

    // Get stageMetadataChecker
    UsdValidationRegistry &registry = UsdValidationRegistry::GetInstance();
    const UsdValidator *validator = registry.GetOrLoadValidatorByName(
            UsdGeomValidatorNameTokens->stageMetadataChecker);
    TF_AXIOM(validator);

    // Create an empty stage
    UsdStageRefPtr usdStage = UsdStage::CreateInMemory();

    // Validate knowing there is no default prim
    UsdValidationErrorVector errors = validator->Validate(usdStage);

    // Verify the correct error is returned
    TF_AXIOM(errors.size() == 2);
    TF_AXIOM(errors[0].GetType() == UsdValidationErrorType::Error);
    TF_AXIOM(errors[0].GetSites().size() == 1);
    TF_AXIOM(errors[0].GetSites()[0].IsValid());
    const std::string expectedErrorMsg = "Stage has missing or invalid defaultPrim.";
    TF_AXIOM(errors[0].GetMessage() == expectedErrorMsg);
}

int
main()
{
    TestUsdStageMetadata();

    std::cout << "OK\n";
}
```

### Update plugInfo.json

Include at the top level of Plugins: 

```
"Plugins": [
    "Info": {
        ...
    },
    "Validators": {
        "StageMetadataChecker": {
            "doc": "All stages should declare their 'upAxis' and 'metersPerUnit' and stages meant for consumer-level packaging should always have upAxis set to 'Y'."
        },
        "keywords": [
            "UsdGeomValidators"
        ]
    }
]

````

### Update CMakeLists.txt

#### Validator Tokens

Include in `pxr_library` under `PUBLIC_CLASSES`

```
pxr_library(usdGeom
    LIBRARIES
        ...

    INCLUDE_DIRS
        ...

    PUBLIC_CLASSES
        ...
        validatorTokens
        ...
```

#### Validator

Since we only add a .cpp for the validator, this gets added under `CPP_FILES`

```
pxr_library(usdGeom
    LIBRARIES
        ...

    INCLUDE_DIRS
        ...

    PUBLIC_CLASSES
        ...
    
    PUBLIC_HEADERS
        ...
    
    CPP_FILES
        validators
```


#### Unit Test

Build Test:

```
pxr_build_test(testUsdGeomValidators
    LIBRARIES
        usd
        usdGeom
    CPPFILES
        testenv/testUsdGeomValidators.cpp
)
```

Register Test:

```
pxr_register_test(testUsdGeomValidators
    COMMAND "${CMAKE_INSTALL_PREFIX}/tests/testUsdGeomValidators"
    EXPECTED_RETURN_CODE 0
)
```