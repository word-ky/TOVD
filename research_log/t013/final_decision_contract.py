"""T013-DEC1: metadata-only disclosure contract; no metric computation or I/O."""

VERSION = 'T013-DEC1-v1'
FREEZE = '6fec32243985ccc808123d851abf5f3dea10af99'
RUN = '20260912-210355-tovd-native30-primary'
RELEASE = '20260912-210306-tovd-native30-primary-freeze'
CONDITIONS = ['clean', 'gaussian_noise', 'motion_blur', 'fog', 'jpeg_compression']
VOCABS = ['V0', 'Vhard30', 'Vrand30']
METRICS = ['AP', 'AP50', 'AR', 'AR50', 'canonical_fp_per_image',
           'distractor_fp_per_image', 'canonical_recall', 'localization_recall']
FAMILIES = ['distractor_fp_excess_increase',
            'classification_beyond_localization_excess_drop',
            'matched_localization_margin_excess_shrinkage']
PROVENANCE_FIELDS = ['environment_sha256', 'freeze_sha256', 'plan_sha256',
                     'analysis_sha256', 'coco_sha256', 'diagnostics_sha256',
                     'vocabulary_sha256', 'selection_sha256', 'annotations_sha256',
                     'image_manifest_sha256', 'checkpoint_sha256', 'native_source_revision',
                     'state_before_sha256', 'state_after_sha256', 'run_receipt_sha256',
                     'cache_manifest_sha256', 'results_sha256', 'paired_draws_sha256',
                     'bootstrap_samples_sha256', 'diagnostics_per_image_sha256']
BLOCKED = 'BLOCKED_NO_SCIENTIFIC_INTERPRETATION'
INVALID = 'PROTOCOL_INVALID_NO_SCIENTIFIC_INTERPRETATION'
COHERENT = 'GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_COHERENT'
UNRESOLVED = 'GROUNDING_DUAL_SHIFT_SUPPORTED_MECHANISM_UNRESOLVED'
NEGATIVE = 'GROUNDING_PRIMARY_NOT_SUPPORTED'


def require(condition, path):
    if not condition:
        raise ValueError('Incomplete or invalid disclosure: ' + path)


def field(obj, key, path):
    require(isinstance(obj, dict) and key in obj, path + '.' + key)
    return obj[key]


def text(value, path):
    require(isinstance(value, str) and bool(value.strip()), path)


def boolean(value, path):
    require(type(value) is bool, path)


def tensor(value, shape, path):
    if shape:
        require(isinstance(value, list) and len(value) == shape[0], path)
        for i, item in enumerate(value):
            tensor(item, shape[1:], f'{path}[{i}]')
    else:
        # Preserve frozen NaNs (undefined support), never impute or filter them.
        require(type(value) in (int, float), path)


def interval(value, shape, path):
    # Frozen interval() returns None when any input replicate is nonfinite.
    if value is not None:
        tensor(value, [2] + shape, path)


def decide(summary):
    """Validate completed-summary disclosure and return the Lead's fixed state.

    Evidence statuses are supplied FIN1/replay receipts, not verified anew here.
    Non-PASS evidence can be reported without fabricating final result tables.
    Gate3/4 Lead judgments must be supplied explicitly; no research acceptance.
    """
    require(field(summary, 'contract_version', 'summary') == VERSION, 'contract_version')
    evidence = field(summary, 'evidence', 'summary')
    statuses = []
    for name in ('fin1', 'full_cache_replay'):
        item = field(evidence, name, 'evidence')
        status = field(item, 'status', name)
        require(status in ('PASS', 'FAIL', 'PENDING', 'NOT_RUN'), name + '.status')
        text(field(item, 'receipt_ref', name), name + '.receipt_ref')
        statuses.append(status)
    if statuses != ['PASS', 'PASS']:
        return BLOCKED

    provenance = field(summary, 'provenance', 'summary')
    for key, expected in [('run_id', RUN), ('freeze_commit', FREEZE), ('release_id', RELEASE)]:
        require(field(provenance, key, 'provenance') == expected, 'provenance.' + key)
    for key in PROVENANCE_FIELDS:
        text(field(provenance, key, 'provenance'), 'provenance.' + key)

    result = field(summary, 'results', 'summary')
    for key, expected in [('kind', 'T013-NATIVE30'), ('image_count', 1000),
                          ('conditions', CONDITIONS), ('vocabularies', VOCABS),
                          ('metric_order', METRICS), ('replicates', 1000), ('seed', 20260913)]:
        require(field(result, key, 'results') == expected, 'results.' + key)
    tensor(field(result, 'point_metrics', 'results'), [5, 3, 8], 'results.point_metrics')
    interval(field(result, 'metric_ci95', 'results'), [5, 3, 8], 'results.metric_ci95')
    tensor(field(result, 'margin_common_localized_gt_counts', 'results'), [4],
           'results.margin_common_localized_gt_counts')

    assessment = field(result, 'assessment', 'results')
    for key in ('D_AP50', 'A_AP50'):
        tensor(field(assessment, key, 'assessment'), [4, 3], key)
        interval(field(assessment, key + '_ci95', 'assessment'), [4, 3], key + '_ci95')
    tensor(field(assessment, 'hard_minus_random', 'assessment'), [4], 'hard_minus_random')
    interval(field(assessment, 'hard_minus_random_ci95', 'assessment'), [4],
             'hard_minus_random_ci95')
    for key in ('mean_A_hard', 'mean_hard_minus_random'):
        tensor(field(assessment, key, 'assessment'), [], key)
        interval(field(assessment, key + '_ci95', 'assessment'), [], key + '_ci95')
    for key in ('gate1', 'gate2', 'gate3_statistical_support', 'gate4_recorded_checks'):
        boolean(field(assessment, key, 'assessment'), key)
    material = field(assessment, 'gate1_corruptions', 'assessment')
    require(isinstance(material, list) and len(material) == 4, 'gate1_corruptions')
    for value in material:
        boolean(value, 'gate1_corruptions')
    text(field(assessment, 'research_acceptance', 'assessment'), 'research_acceptance')
    diagnostics = field(assessment, 'gate3_diagnostics', 'assessment')
    for family in FAMILIES:
        item = field(diagnostics, family, 'gate3_diagnostics')
        tensor(field(item, 'per_corruption', family), [4], family + '.per_corruption')
        tensor(field(item, 'mean', family), [], family + '.mean')
        interval(field(item, 'mean_ci95', family), [], family + '.mean_ci95')
        count = field(item, 'positive_corruptions', family)
        require(type(count) is int and 0 <= count <= 4, family + '.positive_corruptions')
        boolean(field(item, 'statistical_support', family), family + '.statistical_support')

    lead = field(summary, 'lead_review', 'summary')
    for key in ('gate3_coherent', 'gate4'):
        boolean(field(lead, key, 'lead_review'), 'lead_review.' + key)
    for key in ('review_ref', 'gate3_rationale', 'gate4_history_audit_ref'):
        text(field(lead, key, 'lead_review'), 'lead_review.' + key)
    # Recorded runtime checks and the Lead's Git/protocol audit both matter.
    if not assessment['gate4_recorded_checks'] or not lead['gate4']:
        return INVALID
    if not assessment['gate1'] or not assessment['gate2']:
        return NEGATIVE
    return COHERENT if lead['gate3_coherent'] else UNRESOLVED
