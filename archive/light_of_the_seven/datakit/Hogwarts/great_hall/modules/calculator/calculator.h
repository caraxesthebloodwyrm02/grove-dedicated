#ifndef GREAT_HALL_CALCULATOR_H
#define GREAT_HALL_CALCULATOR_H

/*
  calculator.h — Great Hall "calculator" module (C)

  Purpose:
    - Define criteria and weights
    - Accept option ratings (per-criterion)
    - Normalize + score + rank options
    - Export/import JSON compatible with the Great Hall shared contract

  Notes:
    - This is a skeleton header intended to be implemented in calculator.c.
    - JSON is carried as UTF-8 text; integrate a JSON library in calculator.c.
    - Ownership rules: unless specified, strings passed in are copied.
*/

#include <stddef.h> /* size_t */

#ifdef __cplusplus
extern "C" {
#endif

/* ---------------------------- Versioning ---------------------------- */

#define GH_CALCULATOR_VERSION_MAJOR 1
#define GH_CALCULATOR_VERSION_MINOR 0
#define GH_CALCULATOR_VERSION_PATCH 0

/* ----------------------------- Status ------------------------------ */

typedef enum gh_calculator_status {
  GH_CALC_OK = 0,
  GH_CALC_ERR_INVALID_ARGUMENT = 1,
  GH_CALC_ERR_OUT_OF_MEMORY = 2,
  GH_CALC_ERR_PARSE = 3,
  GH_CALC_ERR_NOT_FOUND = 4,
  GH_CALC_ERR_BUFFER_TOO_SMALL = 5,
  GH_CALC_ERR_INTERNAL = 100
} gh_calculator_status_t;

/* Convert a status code to a stable string literal (never NULL). */
const char* gh_calc_status_str(gh_calculator_status_t status);

/* --------------------------- Shared types -------------------------- */

typedef enum gh_criteria_type {
  GH_CRIT_BOOL = 0,
  GH_CRIT_NUMBER = 1,
  GH_CRIT_TEXT = 2
} gh_criteria_type_t;

typedef enum gh_criteria_polarity {
  GH_POLARITY_HIGHER_IS_BETTER = 0,
  GH_POLARITY_LOWER_IS_BETTER = 1,
  GH_POLARITY_NEUTRAL = 2
} gh_criteria_polarity_t;

typedef enum gh_normalization_mode {
  /*
    Normalize numeric criteria into [0,1] prior to weighting.

    NONE:          use raw numeric value as "normalized" (caller must ensure comparability)
    MIN_MAX:       (x - min) / (max - min)
    Z_SCORE:       (x - mean) / stddev (optionally squashed by implementation)
    CLAMP_0_1:     clamp provided normalized values into [0,1]
  */
  GH_NORM_NONE = 0,
  GH_NORM_MIN_MAX = 1,
  GH_NORM_Z_SCORE = 2,
  GH_NORM_CLAMP_0_1 = 3
} gh_normalization_mode_t;

/* Criteria definition (stored/canonical). */
typedef struct gh_criterion_def {
  char* id;               /* owned */
  char* name;             /* owned */
  char* description;      /* optional, owned (may be NULL) */
  gh_criteria_type_t type;

  double weight;          /* >= 0 */
  gh_criteria_polarity_t polarity;

  /* Numeric range hint (only meaningful when type == GH_CRIT_NUMBER) */
  int has_range;          /* 0/1 */
  double range_min;
  double range_max;
} gh_criterion_def_t;

/* Option definition. */
typedef struct gh_option_def {
  char* id;               /* owned */
  char* label;            /* owned */
  char* notes;            /* optional, owned (may be NULL) */
} gh_option_def_t;

/* -------------------------- Rating values -------------------------- */

/*
  Ratings are stored as a tagged union.
  - BOOL: 0 or 1
  - NUMBER: double
  - TEXT: arbitrary string (may be used for qualitative notes; scoring may ignore or map via rules)
*/
typedef enum gh_rating_kind {
  GH_RATING_UNSET = 0,
  GH_RATING_BOOL = 1,
  GH_RATING_NUMBER = 2,
  GH_RATING_TEXT = 3
} gh_rating_kind_t;

typedef struct gh_rating_value {
  gh_rating_kind_t kind;
  union {
    int b;
    double n;
    char* t; /* owned by calculator workspace when set via API */
  } v;
} gh_rating_value_t;

/* ------------------------- Result structures ----------------------- */

typedef struct gh_score_contribution {
  char* criteria_id;   /* owned in exported results; view in getters */
  double contribution; /* weight * normalized (or weight * mapped) */

  /* For transparency */
  gh_rating_value_t raw; /* view; raw.t may be NULL if not applicable */
  double normalized;     /* implementation-defined normalization output */
} gh_score_contribution_t;

typedef struct gh_option_score {
  char* option_id;                     /* view */
  double score;                        /* total */
  gh_score_contribution_t* breakdown;  /* array (owned by results object) */
  size_t breakdown_count;
} gh_option_score_t;

/* Opaque handles */
typedef struct gh_calculator gh_calculator_t;
typedef struct gh_calc_results gh_calc_results_t;

/* ------------------------- Workspace lifecycle ---------------------- */

gh_calculator_t* gh_calc_create(void);
void gh_calc_destroy(gh_calculator_t* calc);
void gh_calc_clear(gh_calculator_t* calc);

/* ------------------------- Criteria management ---------------------- */

/*
  Add or replace a criterion definition by id.
  - All strings are copied.
  - weight must be >= 0
*/
gh_calculator_status_t gh_calc_criteria_upsert(
    gh_calculator_t* calc,
    const char* criteria_id,
    const char* name,
    const char* description, /* may be NULL */
    gh_criteria_type_t type,
    double weight,
    gh_criteria_polarity_t polarity,
    int has_range,
    double range_min,
    double range_max
);

gh_calculator_status_t gh_calc_criteria_remove(gh_calculator_t* calc, const char* criteria_id);
size_t gh_calc_criteria_count(const gh_calculator_t* calc);

/* Read-only view by index (0..count-1). Pointers valid until clear/destroy or remove. */
gh_calculator_status_t gh_calc_criteria_get_by_index(
    const gh_calculator_t* calc,
    size_t index,
    gh_criterion_def_t* out_view
);

/* -------------------------- Option management ----------------------- */

gh_calculator_status_t gh_calc_option_upsert(
    gh_calculator_t* calc,
    const char* option_id,
    const char* label,
    const char* notes /* may be NULL */
);

gh_calculator_status_t gh_calc_option_remove(gh_calculator_t* calc, const char* option_id);
size_t gh_calc_option_count(const gh_calculator_t* calc);

gh_calculator_status_t gh_calc_option_get_by_index(
    const gh_calculator_t* calc,
    size_t index,
    gh_option_def_t* out_view
);

/* --------------------------- Ratings matrix ------------------------- */

/*
  Set ratings per (option_id, criteria_id).
  - For TEXT ratings: value is copied.
  - Setting kind = UNSET clears the rating.
*/
gh_calculator_status_t gh_calc_set_rating_bool(
    gh_calculator_t* calc,
    const char* option_id,
    const char* criteria_id,
    int value_0_or_1
);

gh_calculator_status_t gh_calc_set_rating_number(
    gh_calculator_t* calc,
    const char* option_id,
    const char* criteria_id,
    double value
);

gh_calculator_status_t gh_calc_set_rating_text(
    gh_calculator_t* calc,
    const char* option_id,
    const char* criteria_id,
    const char* value_utf8
);

gh_calculator_status_t gh_calc_clear_rating(
    gh_calculator_t* calc,
    const char* option_id,
    const char* criteria_id
);

/*
  Get a read-only rating view.
  - For TEXT, out_view->v.t points into calculator storage (valid until overwritten/cleared/clear/destroy).
*/
gh_calculator_status_t gh_calc_get_rating(
    const gh_calculator_t* calc,
    const char* option_id,
    const char* criteria_id,
    gh_rating_value_t* out_view
);

/* -------------------------- Scoring controls ------------------------ */

/*
  Configure normalization for numeric criteria.
  - mode applies to all numeric criteria by default unless overridden.
  - Per-criterion overrides can be added later (implementation-defined).
*/
gh_calculator_status_t gh_calc_set_normalization_mode(
    gh_calculator_t* calc,
    gh_normalization_mode_t mode
);

/*
  Configure how missing numeric ratings affect scoring.
  - If skip_missing == 1: missing criteria contribute 0 (but weights remain as-is).
  - If renormalize_weights == 1: weights are renormalized per-option over rated criteria only.
    (Only meaningful if skip_missing==1.)
*/
gh_calculator_status_t gh_calc_set_missing_policy(
    gh_calculator_t* calc,
    int skip_missing,
    int renormalize_weights
);

/*
  Configure how bool criteria are mapped into numeric:
  - false_value and true_value are the normalized values used before polarity and weighting.
*/
gh_calculator_status_t gh_calc_set_bool_mapping(
    gh_calculator_t* calc,
    double false_value,
    double true_value
);

/* ----------------------------- Compute ------------------------------ */

/*
  Validate internal invariants:
    - unique IDs
    - weights >= 0
    - numeric ranges consistent when present (min < max)
    - ratings types compatible with criteria types (best-effort)
*/
gh_calculator_status_t gh_calc_validate(const gh_calculator_t* calc);

/*
  Compute results:
    - Produces scores for all options
    - Sorts ranked options descending by score (tie-breaking implementation-defined)
*/
gh_calculator_status_t gh_calc_compute(
    const gh_calculator_t* calc,
    gh_calc_results_t** out_results /* allocated; caller must destroy */
);

void gh_calc_results_destroy(gh_calc_results_t* results);

size_t gh_calc_results_count(const gh_calc_results_t* results);

/* Get ranked result by index (0..count-1). Breakdown is owned by results, view is valid until destroy. */
gh_calculator_status_t gh_calc_results_get_by_index(
    const gh_calc_results_t* results,
    size_t index,
    gh_option_score_t* out_view
);

/* ------------------------------ JSON -------------------------------- */

/*
  JSON conventions (recommended):
    - Import/export integrates with the shared contract keys:
        "criteria_set", "options", "calculator_results"
    - Implementation may also accept a calculator-only object.
*/

gh_calculator_status_t gh_calc_import_json(gh_calculator_t* calc, const char* json_utf8);

/*
  Export:
    - If out_json_utf8 is NULL or out_cap == 0, returns required size in out_required (incl. NUL).
    - Otherwise writes a NUL-terminated JSON string.
*/
gh_calculator_status_t gh_calc_export_json(
    const gh_calculator_t* calc,
    const gh_calc_results_t* results, /* may be NULL to export definitions only */
    char* out_json_utf8,
    size_t out_cap,
    size_t* out_required /* may be NULL */
);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* GREAT_HALL_CALCULATOR_H */