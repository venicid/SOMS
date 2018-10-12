{% set files = salt['pillar.get']('files',) %}
{% set dst_path = salt['pillar.get']('dst_path',) %}
{% set src_path = salt['pillar.get']('src_path',) %}
{% set remote_path = salt['pillar.get']('remote_path',) %}
{% set SALTSRC = salt['pillar.get']('SALTSRC',) %}

backup_dir:
  file.directory:
    - name: {{ dst_path }}
    - makedirs: True
  cmd.run:
    - cwd: {{ remote_path }}
    - name: |
        {% for file in files %}
        /bin/cp -rf {{ file }} {{ dst_path }}
        {% endfor %}
    - unless: test ! -d {{ dst_path }}

file_upload:
  file.recurse:
    - name: {{ remote_path }}
    - source: salt://{{ SALTSRC }}/{{ src_path }}
    - backup: minion
